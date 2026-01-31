from typing import List, Tuple


def postprocess_ocr(
    ocr_outputs: List[Tuple[str, float, Tuple[int, int, int, int]]],
    conf_threshold: float = 0.4
) -> str:
    """
    Sorts characters and builds final plate text
    """

    filtered = [
        (text, bbox)
        for text, conf, bbox in ocr_outputs
        if conf >= conf_threshold
    ]

    if not filtered:
        return ""

    # sort by x-coordinate (left to right)
    filtered.sort(key=lambda x: x[1][0])

    final_text = "".join([t[0] for t in filtered])

    # normalization
    final_text = final_text.replace(" ", "").upper()

    return final_text
