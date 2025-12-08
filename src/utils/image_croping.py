def crop(img, bbox):
    x1, y1, x2, y2 = bbox
    return img[y1:y2, x1:x2]
