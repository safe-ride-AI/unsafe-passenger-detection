class ViolationLogic:
    def __init__(self, unsafe_frame_threshold: int = 1):
        ### in this we check how many number of frames are required to confirm its unsafe 


        self.unsafe_frame_threshold = unsafe_frame_threshold

    def check_violation(self, track_state: dict) -> bool:

        if track_state["violation_confirmed"]:
            return False  # already confirmed, don't re-trigger

        if track_state["unsafe_count"] >= self.unsafe_frame_threshold:
            return True

        return False
