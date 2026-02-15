# app/services/violation_logic.py

class ViolationLogic:
    def __init__(self, unsafe_frame_threshold: int = 5):
        """
        unsafe_frame_threshold:
        Number of consecutive unsafe frames required
        to confirm a violation.
        """
        self.unsafe_frame_threshold = unsafe_frame_threshold

    def check_violation(self, track_state: dict) -> bool:
        """
        Decide whether a violation should be confirmed.

        Input:
            track_state (dict) from TrackStateManager

        Output:
            True if violation confirmed, else False
        """

        if track_state["violation_confirmed"]:
            return False  # already confirmed, don't re-trigger

        if track_state["unsafe_count"] >= self.unsafe_frame_threshold:
            return True

        return False
