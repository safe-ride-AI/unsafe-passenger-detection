from ultralytics import YOLO
import numpy as np
import torch
from typing import List


class VehicleDetector:
    def __init__(self,model_path:str,device:str=None,conf_threshold:float=0.4):
        """
        this class is for vechile model where i load my model
        model_paht 
        threshould
        device
        """

        if device is None: ## checking device type if its gpu run on gpu else on cpu
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

        self.allowed_classes = {
            0:'bus',
            1:'suzuki',
            2:'changchi'
        }

    def detect_and_track(self,frame:np.ndarray)-> List:
        """
        in this fuction 

        input single frame

        return list

        list of dict 
        [
           {
            track_id :int ,
            bbox : [x1,y1,x2,y2]
            class:str
            confidence:float
           }
           ...like of there are multiple objects in signle frame
        ]

        """

        results = self.model.track(
            frame,
            persist=True,
            conf=self.conf_threshold,
            tracker="bytetrack.yaml",
            verbose=False
        )
        ## frame  original images
        ### presist open the memory track it give instrction to model remember the previous image use for tacker help
        #### verbose false dont give us meta data
        #### conf = confidence threshould

        ## model return object , it return list of object for list of images
        ## but here we send single image it send list of object of one
        ### results[0] this is object 
        ### results[0]  consist of original image and boxes
        ### boxes consist of 

        detections = list() ## this will be return

        detections = []

        if results[0].boxes.id is None:
            return detections

        boxes = results[0].boxes

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            if cls_id not in self.allowed_classes:
                continue

            track_id = int(boxes.id[i])
            x1, y1, x2, y2 = map(int, boxes.xyxy[i].tolist())
            confidence = float(boxes.conf[i])

            detections.append({
                "track_id": track_id,
                "bbox": [x1, y1, x2, y2],
                "class": self.allowed_classes[cls_id],
                "confidence": confidence
            })

        return detections
        
 

