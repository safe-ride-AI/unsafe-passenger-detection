import re


class PakistanPlateFormatter:
    """
    Very simple rule-based cleaner:
    - keep only A–Z and 0–9
    - fix common OCR confusions (O→0, I→1 etc.)
    - enforce pattern like AAA-123 or similar
    """

    def __init__(self):
        # mapping to fix common OCR mistakes
        self.map_chars = {
            "O": "0",
            "I": "1",
            "L": "1",
            "Z": "2",
            "S": "5",
            "B": "8",
        }

    def _clean(self, text: str) -> str:
        text = text.upper()
        text = "".join(ch for ch in text if ch.isalnum())

        # fix common confusions
        fixed = []
        for ch in text:
            if ch in self.map_chars:
                fixed.append(self.map_chars[ch])
            else:
                fixed.append(ch)
        return "".join(fixed)

    def format(self, raw_text: str) -> str:
        cleaned = self._clean(raw_text)
        if not cleaned:
            return ""

        # if contains letters + digits, try to put a dash between them
        m = re.match(r"^([A-Z]+)([0-9]+)$", cleaned)
        if m:
            return f"{m.group(1)}-{m.group(2)}"

        # if it’s already something like ABC-123 keep as is
        if re.match(r"^[A-Z]{2,4}-[0-9]{1,4}$", cleaned):
            return cleaned

        # fallback: just return cleaned
        return cleaned
