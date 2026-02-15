class TrackStateManger:
    def __init__(self,max_missing_frames:int=30):

            '''
            max missing frames , 
            number of frmae after which a track is removed if not seen again
            '''

            self.tracks = dict()
            self.max_missing_frames = max_missing_frames

    def update(self,track_id:int , frame_index:int):
            """
            this function will be called when a track_id seen in the current frame.
            """

            if track_id not in self.tracks:
                self.tracks[track_id]={
                    'track_id':track_id,
                    'first_seen':frame_index,
                    'last_seen':frame_index,
                    'unsafe_count': 0,
                    'violation_confirmed':False
                }
            else:
                self.tracks[track_id]['last_seen'] = frame_index

    def increament_unsafe(self,track_id:int):
            " in this fucntion we will increament count of unsafe frame"

            if track_id in self.tracks:
                self.tracks[track_id]['unsafe_count'] +=1

    def reset_unsafe(self,track_id:int):
            if track_id in self.tracks:
                self.tracks[track_id]['unsafe_count'] = 0

    def confirm_violation(self,track_id:int):
            ## mark viloation 

            if track_id in self.tracks:
                self.tracks[track_id]['violation_confirmed']=True

    def is_confirmed(self,track_id:int)-> bool:

            return self.tracks.get(track_id,{}).get("violation_confirmed",False)
        
    def cleanup(self, current_frame_index: int):
            """
            Remove tracks that disappeared for too long.
            """
            to_remove = []

            for track_id, data in self.tracks.items():
                if current_frame_index - data["last_seen"] > self.max_missing_frames:
                    to_remove.append(track_id)

            for track_id in to_remove:
                del self.tracks[track_id]