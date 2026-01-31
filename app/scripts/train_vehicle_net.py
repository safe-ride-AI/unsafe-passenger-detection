from ultralytics import YOLO

DATA_YAML = "data/vehicle/data.yaml"
MODEL = "yolov8n.pt"
EPOCHS = 50
IMG_SIZE = 640


def main():
    model = YOLO(MODEL)

    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        device=0,
        project="results/vehicle",
        name="vehicle_net"
    )


if __name__ == "__main__":
    main()
