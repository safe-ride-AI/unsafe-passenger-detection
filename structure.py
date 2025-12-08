import os

ROOT = ""

folders = [
    f"models",
    f"src/pipeline",
    f"src/detectors",
    f"src/utils",
    f"scripts",
    f"data/samples",
]

files = [
    ##f"{ROOT}/README.md",
    f"requirements.txt",
    f"src/pipeline/safety_pipeline.py",
    f"src/detectors/vehicle.py",
    f"src/detectors/passenger_cls.py",
    f"src/detectors/plate.py",
    f"src/utils/image.py",
    f"src/utils/ocr.py",
    f"scripts/run_image.py",
    f"scripts/run_video.py",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w") as f:
        f.write("")

print("Minimal clean project structure created!")
