import cv2
import numpy as np
from typing import Tuple

def clamp_bbox(
        bbox:Tuple[int,int,int,int],
        img_width:int,
        img_height:int
)->Tuple[int,int,int,int]:
    ### ensure boundeing box stays within image boundraiese

    x1,y1,x2,y2 = bbox

    x1 = max(0,x1)
    y1 = max(0,y1)
    x2 = min(img_width - 1, x2)
    y2 = min(img_height - 1, y2)

    return x1,y1,x2,y2

def crop_vehicle(
        frame:np.ndarray,
        bbox:Tuple[int,int,int,int]
)-> np.ndarray:
    
    ### croping vechile from frame using bounding box

    h,w = frame.shape[:2]
    x1,y1,x2,y2 = clamp_bbox(bbox,w,h)

    return frame[y1:y2,x1:x2]

def resize_and_pad(
        image:np.ndarray,
        target_size:Tuple[int,int] = (224,224),
        pad_color:Tuple[int,int,int] = (0,0,0)
)-> np.ndarray:
    target_w,target_h = target_size
    h,w = image.shape[:2]

    if h == 0 or w == 0:
        raise ValueError("Invalid image with zero dimension")

    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(image, (new_w, new_h))

    padded = np.full(
        (target_h, target_w, 3),
        pad_color,
        dtype=np.uint8
    )

    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2

    padded[
        y_offset:y_offset + new_h,
        x_offset:x_offset + new_w
    ] = resized

    return padded
