from app.pipelines.frame_reader import VideoFrameReader
from app.models.vehicle.vehicle_detector import VehicleDetector
from app.services.tracking_state import TrackStateManger
from app.utils.image import crop_vehicle, resize_and_pad
from app.models.unsafe_behavior.efficientnet import UnsafeBehaviorClassifier
from app.services.violation_logic import ViolationLogic
from app.models.license_plate.lp_detector import LicensePlateDetector
from app.models.ocr.ocr_engine import OCRRecognizer
from app.services.storage_service import StorageService


class VideoPipeline:
    def __init__(self, config: dict):

         ## where config is direction recive from  video_dection 
        self.reader = VideoFrameReader(config["video_source"]) ## frame reader object

        self.detector = VehicleDetector(
            model_path=config["vehicle_model"],
            device=config["device"]
        )

        self.track_state = TrackStateManger(
            max_missing_frames=config.get("max_missing_frames", 30)
        )

        self.unsafe_classifier = UnsafeBehaviorClassifier(
            weights_path=config["unsafe_model"],
            device=config["device"],
            threshold=config.get("unsafe_threshold", 0.5)
        )

        self.violation_logic = ViolationLogic(
            unsafe_frame_threshold=config.get("unsafe_frame_threshold", 1)
        )

        self.lp_detector = LicensePlateDetector(
            model_path=config["lp_model"],
            device=config["device"]
        )

        # Pretrained OCR (EasyOCR)
        self.ocr = OCRRecognizer(
            languages=["en"],
            gpu=config.get("device") == "cuda"
        )

        self.storage = StorageService(
            base_dir=config.get("evidence_dir", "data/violations")
        )

    def run(self):
        for frame, meta in self.reader.frames(): ## which will return Tuple consist of frame and meta = dict 
            frame_index = meta["frame_index"] 

            detections = self.detector.detect_and_track(frame) ### call for vehilce dector of given frame , so it will return list and list consist of directoy and directoy will have each vehiicle data that is been detected

            for det in detections:  ## to get each directory from list that is been detected by vehicle detector
                track_id = det["track_id"]
                bbox = det["bbox"]   

                # 1️ Update tracking memory
                self.track_state.update(track_id, frame_index)   ### update the track id that of detected vehicle

                # 2️Crop vehicle
                vehicle_crop = crop_vehicle(frame, bbox)   ### croping detected vehicle from actul frame 
                vehicle_crop = resize_and_pad(vehicle_crop, (224, 224))  ### Add pad so it does not cut passenger sitting on tops and hanging on side

                # 3️ Unsafe classification
                result = self.unsafe_classifier.predict(vehicle_crop)  ### send crop vehicle to classification to classify wether its save vs unsafe

                if result["label"] == "unsafe":
                    self.track_state.increament_unsafe(track_id)
                else:
                    self.track_state.reset_unsafe(track_id)   ###### i think i should remove this bcz if one image its unsafe it should remain unsafe even in other frames its safe

                track = self.track_state.tracks[track_id]  ##### getting track id from track dictionary

                # 4️ Temporal confirmation
                if self.violation_logic.check_violation(track):  ### checking the violation of tracking  if its unsafe get its numberplate

                    # Mark confirmed to avoid duplicate triggering
                    self.track_state.confirm_violation(track_id) 

                    plate_crop = None
                    plate_text = None

                    # 5️ License plate detection
                    plate_result = self.lp_detector.detect(vehicle_crop)

                    if plate_result:
                        px1, py1, px2, py2 = plate_result["bbox"]
                        plate_crop = vehicle_crop[py1:py2, px1:px2]

                        # 6️ Pretrained OCR
                        plate_text = self.ocr.recognize(plate_crop)

                    # 7️ Save evidence (disk only)
                    self.storage.save_violation(
                        track_id=track_id,
                        timestamp_sec=meta["timestamp_sec"],
                        unsafe_confidence=result["confidence"],
                        vehicle_crop=vehicle_crop,
                        plate_crop=plate_crop,
                        plate_text=plate_text
                    )

            # Cleanup stale tracks
            self.track_state.cleanup(frame_index)