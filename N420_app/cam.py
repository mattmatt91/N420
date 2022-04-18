
import io
from datetime import date, datetime, timedelta
from time import time, sleep
import picamera
from base_camera import BaseCamera

import numpy as np
from pathlib import Path
import os
from threading import Thread
from time import sleep

class Cam(BaseCamera):
    h = 1024 
    cam_res = (int(h),int(0.75*h)) 
    cam_res = (int(16*np.floor(cam_res[1]/16)),int(32*np.floor(cam_res[0]/32)))
    capture_interval = timedelta(minutes=20)
    last_capture = datetime.now()- capture_interval
    path =os.path.join("data" ,"pictures")
    Path(path).mkdir(parents=True, exist_ok=True)
    
    data = np.empty((cam_res[0],cam_res[1],3),dtype=np.uint8)

    @staticmethod
    def save_img_loop():
        def update():
            while True:
                if datetime.now() >= Cam.last_capture + Cam.capture_interval:
                    Cam()
        Thread(target=update).start()
        

    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            camera.resolution = (Cam.cam_res[1],Cam.cam_res[0])
            camera.rotation = 270
            # let camera warm up
            sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                            use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                if datetime.now() >= Cam.last_capture + Cam.capture_interval: 
                    Cam.safe_frame(camera)
                    print('saving image')
                    Cam.last_capture = datetime.now()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

        
    @classmethod  
    def safe_frame(cls,camera):
        name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + ".png"
        path = os.path.join(cls.path, name)
        print(path)
        camera.capture(path)




if __name__ == '__main__':
    print('starting')
    cam = Cam()
    print('cam generated')
    while True:
        try:
            sleep(1)
            cam.get_frame()
        except:
            pass