import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image
import cv2

class PassengerClassifier:
    def __init__(self, ckpt_path, device="cuda"):
        checkpoint = torch.load(ckpt_path, map_location=device)

        # labels
        self.class_to_idx = checkpoint["class_to_idx"]
        self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}

        # model
        self.model = EfficientNet.from_pretrained("efficientnet-b0")
        num_features = self.model._fc.in_features
        self.model._fc = nn.Linear(num_features, 2)
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.to(device)
        self.model.eval()

        self.device = device

        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, crop_bgr):
        img_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        tensor = self.preprocess(pil_img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            out = self.model(tensor)
            probs = torch.softmax(out, dim=1)[0]
            conf, cls_idx = torch.max(probs, dim=0)

        label = self.idx_to_class[cls_idx.item()]
        return label, float(conf.item())
