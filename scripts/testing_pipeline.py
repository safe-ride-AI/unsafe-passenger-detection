from src.detectors.vehicle import VehicleDetector
from src.detectors.passenger_cls import PassengerClassifier
from src.detectors.plate import PlateDetector
from src.pipeline.safety_pipeline import SafetyPipeline

vehicle = VehicleDetector("models/vehicle_yolo.pt")
passenger = PassengerClassifier("models/passenger_cls.pth")
plate = PlateDetector("models/plate_yolo.pt")

pipeline = SafetyPipeline(vehicle, passenger, plate)

output = pipeline.run("test_images/test1.jpg")
print(output)
