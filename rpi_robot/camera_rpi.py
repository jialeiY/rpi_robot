import threading
import picamera
import io
import threading
import time

class Camera(object):
    thread=None
    frame=None
    last_access=0


    def initialize(self):
        if Camera.thread is None:
            Camera.thread=threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access=time.time()
        self.initialize()
        return self.frame
    @classmethod
    def _thread(cls):        

        with picamera.PiCamera() as camera:
           
            camera.resolution=(320,240)
            camera.hflip=True
            camera.framerate=5
            stream=io.BytesIO()            
            for foo in camera.capture_continuous(stream,format='jpeg',\
                                                use_video_port=True):
                
                stream.seek(0)
                cls.frame=stream.read()

                if time.time()-cls.last_access>10:
                    break
                stream.seek(0)
                stream.truncate()
           
        
        cls.thread=None
