import torch
import torch.nn as nn
import numpy as np
import cv2
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image
from .schema import UnsafeBehaviorOutput


class UnsafeBehaviorClassifier:
    """
    EfficientNet-based Safe vs Unsafe classifier
    (loads checkpoint with model_state + class_to_idx)
    """

    def __init__(self, weights_path: str, device: str = "cpu"):
        checkpoint = torch.load(weights_path, map_location=device)

        # labels
        self.class_to_idx = checkpoint["class_to_idx"]
        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}

        # model
        self.model = EfficientNet.from_pretrained("efficientnet-b0")
        num_features = self.model._fc.in_features
        self.model._fc = nn.Linear(num_features, 2)

        # ✅ LOAD CORRECT KEY
        self.model.load_state_dict(checkpoint["model_state"])

        self.model.to(device)
        self.model.eval()
        self.device = device

        # preprocessing (MATCH TRAINING)
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    @torch.no_grad()
    def predict(self, crop_bgr: np.ndarray) -> UnsafeBehaviorOutput:
        img_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        tensor = self.preprocess(pil_img).unsqueeze(0).to(self.device)

        out = self.model(tensor)
        probs = torch.softmax(out, dim=1)[0]
        conf, cls_idx = torch.max(probs, dim=0)

        label = self.idx_to_class[cls_idx.item()]

        return UnsafeBehaviorOutput(
            is_unsafe=(label != "safe"),
            confidence=float(conf.item())
        )
