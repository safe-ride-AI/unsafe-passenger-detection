import cv2
import numpy as np
from typing import Generator, Tuple

class VideoFrameReader:
    def __init__(self,source:str):

        ## this fuction will receive source file during object creation
        self.source = source
        self.cap = cv2.VideoCapture(source) ## it will read the file of video

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source : {source}")
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) ## asking how many frames from video in sec
        if self.fps == 0: ## if it returns  zero so we assign be defult 25
            self.fps = 25
    
    def frames(self)-> Generator[Tuple[np.ndarray,dict],None,None]:
        """
        this is frames function where i will return generator which save memory
        bcz list load entir list onto memory where generator return one by one

        generator[yeild,input,return]
        so we return tuple in yeild , and input none , final return none
        """

        frame_index = 0

        while True:

            ret , frame = self.cap.read()
            ## it return Tuple which has boleean value and frame
            ## bolean will tell us where has frame or not if not False so that mean video stop
            if not ret: ## this way we break the condition
                break
            
            timestamp_sec = frame_index/self.fps

            meta = {
                "frame_index" : frame_index,
                "timestamp_sec": timestamp_sec,
            }
            
            yield frame,meta

            frame_index +=1

        self.cap.release()