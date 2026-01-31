import torch
import numpy as np
from .schema import UnsafeBehaviorOutput


class UnsafeBehaviorClassifier:
    def __init__(self, weights_path: str, device: str = "cpu"):
        self.device = device
        self.model = torch.load(weights_path, map_location=device)
        self.model.eval()

    def preprocess(self, image: np.ndarray) -> torch.Tensor:
        img = torch.from_numpy(image).permute(2, 0, 1).float()
        img = img / 255.0
        return img.unsqueeze(0).to(self.device)

    def predict(self, image: np.ndarray) -> UnsafeBehaviorOutput:
        x = self.preprocess(image)

        with torch.no_grad():
            prob_unsafe = float(self.model(x))

        return UnsafeBehaviorOutput(
            is_unsafe=prob_unsafe >= 0.5,
            confidence=prob_unsafe
        )
