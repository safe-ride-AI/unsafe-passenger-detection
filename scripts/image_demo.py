# scripts/run_image_demo.py

import os
import cv2
import matplotlib.pyplot as plt

from pipeline.safety_pipeline import (
    VehicleDetector,
    PlateDetector,
    PassengerClassifier,
    SafetyPipeline,
    PlateOCR,
    PakistanPlateFormatter
)
from utils.image_croping import crop


def visualize_pipeline_on_image(pipeline: SafetyPipeline, img_path: str):
    res = pipeline.run_on_image(img_path)

    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Cannot read image: {img_path}")

    img_draw = img.copy()
    H, W = img.shape[:2]

    print("\n========== PIPELINE RESULT ==========")
    print("Image:", res["image_path"])
    print("Size: ", res["image_size"])
    print("Vehicles detected:", len(res["vehicles"]))

    # We'll show up to first vehicle and first plate visually
    first_vehicle_crop = None
    first_plate_crop = None
    first_plate_text = None

    for i, v in enumerate(res["vehicles"]):
        x1, y1, x2, y2 = v["vehicle_bbox"]
        unsafe = v["unsafe"]
        label = v["passenger_label"]
        cls_conf = v["passenger_conf"]
        plates = v["plates"]

        color = (0, 255, 0)  # safe -> green
        if unsafe:
            color = (0, 0, 255)  # unsafe -> red

        plate_text = "no-plate"
        if len(plates) > 0:
            p0 = plates[0]
            plate_text = p0["clean_text"] or p0["raw_text"] or "plate?"
            if first_plate_crop is None:
                # reconstruct absolute crop for visualization
                vx1, vy1, vx2, vy2 = v["vehicle_bbox"]
                px1, py1, px2, py2 = p0["plate_bbox"]
                vehicle_crop = crop(img, (vx1, vy1, vx2, vy2))
                first_vehicle_crop = vehicle_crop
                first_plate_crop = crop(vehicle_crop, (px1, py1, px2, py2))
                first_plate_text = plate_text

        text = f"{label} ({cls_conf:.2f}) | {plate_text}"

        # draw box on main image
        cv2.rectangle(img_draw, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            img_draw,
            text,
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA
        )

        print(f"\nVehicle #{i+1}")
        print("  bbox:", v["vehicle_bbox"])
        print("  unsafe:", unsafe)
        print("  passenger_label:", label, "conf:", cls_conf)
        print("  plates:", len(plates))
        for j, p in enumerate(plates):
            print(f"    plate #{j+1}",
                  "| bbox:", p["plate_bbox"],
                  "| raw:", p["raw_text"],
                  "| clean:", p["clean_text"],
                  "| ocr_conf:", p["ocr_conf"])

    # ---- Matplotlib visualization ----
    # Subplots: [original, vehicle crop, plate crop]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Original with boxes
    img_rgb = cv2.cvtColor(img_draw, cv2.COLOR_BGR2RGB)
    axs[0].imshow(img_rgb)
    axs[0].set_title("Original + detections")
    axs[0].axis("off")

    # First vehicle crop
    if first_vehicle_crop is not None:
        v_rgb = cv2.cvtColor(first_vehicle_crop, cv2.COLOR_BGR2RGB)
        axs[1].imshow(v_rgb)
        axs[1].set_title("First vehicle crop")
    else:
        axs[1].text(0.5, 0.5, "No vehicle crop", ha="center", va="center")
    axs[1].axis("off")

    # First plate crop
    if first_plate_crop is not None:
        p_rgb = cv2.cvtColor(first_plate_crop, cv2.COLOR_BGR2RGB)
        axs[2].imshow(p_rgb)
        title = "Plate crop"
        if first_plate_text:
            title += f"\nOCR: {first_plate_text}"
        axs[2].set_title(title)
    else:
        axs[2].text(0.5, 0.5, "No plate crop", ha="center", va="center")
    axs[2].axis("off")

    plt.tight_layout()
    plt.show()


def main():
    device = "cuda" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "cpu"
    print("Using device:", device)

    # YOU ADJUST THESE PATHS
    vehicle_model_path = "models/vehicle_yolo.pt"
    plate_model_path = "models/plate_yolo.pt"
    passenger_ckpt_path = "models/passenger_cls_efficientnet_b0_best.pth"

    vehicle_detector = VehicleDetector(vehicle_model_path, device=device)
    plate_detector = PlateDetector(plate_model_path, device=device)
    passenger_classifier = PassengerClassifier(passenger_ckpt_path, device=device)

    plate_ocr = PlateOCR(lang_list=['en'], gpu=(device == "cuda"))
    plate_formatter = PakistanPlateFormatter()

    pipeline = SafetyPipeline(
        vehicle_detector=vehicle_detector,
        passenger_classifier=passenger_classifier,
        plate_detector=plate_detector,
        plate_ocr=plate_ocr,
        plate_formatter=plate_formatter
    )

    test_img = "samples/test1.jpg"   # change to your test frame path
    visualize_pipeline_on_image(pipeline, test_img)


if __name__ == "__main__":
    main()
