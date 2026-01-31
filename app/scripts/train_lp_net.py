from ultralytics import YOLO

DATA_YAML = "data/license_plate/data.yaml"
MODEL = "yolov8n.pt"
EPOCHS = 40
IMG_SIZE = 640


def main():
    model = YOLO(MODEL)

    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        device=0,
        project="results/license_plate",
        name="lp_net"
    )


if __name__ == "__main__":
    main()
