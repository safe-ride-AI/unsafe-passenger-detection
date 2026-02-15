# app/models/passenger_classifier.py

import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2

class UnsafeBehaviorClassifier:
    def __init__(
        self,
        weights_path: str,
        device: str = "cpu",
        threshold: float = 0.5
    ):
        """
        weights_path: Path to the .pth file (e.g., 'passenger_cls_best.pth')
        """
        self.device = device
        self.threshold = threshold

        print(f"[PassengerClassifier] Loading model on {self.device}...")

        # 1. Load Architecture (Must match 'efficientnet_pytorch' from training)
        self.model = EfficientNet.from_name('efficientnet-b0')
        
        # 2. Match the Output Layer (2 classes: safe, unsafe)
        num_features = self.model._fc.in_features
        self.model._fc = nn.Linear(num_features, 2)

        # 3. Load Weights (Handling the dictionary wrapper)
        checkpoint = torch.load(weights_path, map_location=self.device)

        if "model_state" in checkpoint:
            state_dict = checkpoint["model_state"]
            # Try to read class names from file, otherwise default
            self.class_names = checkpoint.get("class_to_idx", {'safe': 0, 'unsafe': 1})
        else:
            state_dict = checkpoint
            self.class_names = {'safe': 0, 'unsafe': 1}

        # Create reverse lookup (0 -> 'safe')
        self.idx_to_class = {v: k for k, v in self.class_names.items()}

        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

        # 4. Define Transform (Must match training size)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image: np.ndarray):
        """
        Input:
            image: np.ndarray (OpenCV BGR image, usually a crop of a person)
        Output:
            dict { label: str, confidence: float }
        """
        # Safety check: If crop is empty (size 0), return unknown
        if image is None or image.size == 0:
            return {"label": "unknown", "confidence": 0.0}

        # Convert BGR (OpenCV) → RGB (PIL)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        # Preprocess
        tensor = self.transform(pil_image)
        tensor = tensor.unsqueeze(0).to(self.device)

        # Inference
        with torch.no_grad():
            outputs = self.model(tensor)
            probs = torch.softmax(outputs, dim=1) # Convert logits to 0-1 probability
            confidence, class_idx = torch.max(probs, dim=1)

        # Get readable label
        idx = class_idx.item()
        label = self.idx_to_class.get(idx, "unknown")
        
        return {
            "label": label,          # "safe" or "unsafe"
            "confidence": confidence.item() # e.g., 0.95
        }