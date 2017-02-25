import time
import os
import urllib
import io
from PIL import Image,ImageDraw,ImageFont,ImageOps
import threading

from Adafruit_LED_Backpack import Matrix8x16


class LedDisplay(object):
    _thread=None
    _t_stop=None    

    def __init__(self,brightness=1):
        self.base_path=os.path.dirname(os.path.realpath(__file__))
        self.display=Matrix8x16.Matrix8x16()
        self.display.begin()    
        self.display.set_brightness(brightness)
        #self.clear_display()      
        self.stop_led()
        
    def draw_template(self,template):
        #self.display.clear()
        template=template.strip().split('\n')[::-1]
        #print template
        for x,row in enumerate(template):
            for y,col in enumerate(row):
                self.display.set_pixel(x,y,int(col))
                self.display.write_display()
    
    def draw_text(self,word):
        im_len=len(word)*6
        word+='.' if word[-1]!='.' else ''
        image=Image.new('1',(im_len+6 if im_len>16 else 16,8))
        draw=ImageDraw.Draw(image)
        font=ImageFont.load(self.base_path+'/fonts/slkscr.pil')      
        draw.text((0,-2),word,fill=1,font=font)
        image=image.rotate(-90)
       
        if draw.textsize(word)[0]<=16:
            #print draw.textsize(word),image.size
            self.display.set_image(image)
            self.display.write_display()
        else:      
            images=self.display.vertical_scroll(image,padding=False)
            LedDisplay._t_stop=threading.Event()
            LedDisplay._thread=threading.Thread(target=self._loop_display,\
                                                    args=(images,))
            #print LedDisplay._t_stop,LedDisplay._thread
            LedDisplay._thread.start()
    def _loop_display(self,images):
        #print LedDisplay._t_stop
        while not LedDisplay._t_stop.is_set():
            for im in images:
                self.display.set_image(im)
                self.display.write_display()
                time.sleep(0.2)     
            #time.sleep(0.2)
        LedDisplay._thread=None
        LedDisplay._t_stop=None

    def stop_led(self):
        #print 222,LedDisplay._thread
        if LedDisplay._t_stop:
            LedDisplay._t_stop.set()
            while LedDisplay._thread:
                time.sleep(0.1)
        self.display.clear()
        self.clear_display()
    def draw_emoji(self,img=None,url=None):
        #self.display.clear()
        if url:
            url=urllib.urlopen(url)
            f=io.BytesIO(url.read())
            image=Image.open(f)
            url.close()
            #ori_w,ori_h=image.size
            #image=image.rotate(-90)
            #image=image.split()[1]
            #image=image.point(lambda i: 255 if i>20 else 0)
            #image=image.resize((int(ori_w*16/ori_h),16))                
            #image.save(emoji_path+'2/'+im[:-4]+'_2.png')

        else:
            emoji_path=self.base_path+"/static/img/emoji/"            

            image=Image.open(os.path.join(emoji_path,img)) 
            images=self.display.horizontal_scroll(image)
                            
            LedDisplay._t_stop=threading.Event()
            LedDisplay._thread=threading.Thread(target=self._loop_display,
                                                    args=(images,))
            LedDisplay._thread.start()
    def draw_pixel(self,x,y):
        
        self.display.clear()
        self.display.set_pixel(x,y,1)
        self.display.write_display()
        #time.sleep(1)

    def clear_pixel(self,x,y):
        self.display.clear()
        self.display.set_pixel(x,y,0)
        self.display.write_display()

    def clear_display(self):
        self.display.clear()
        for x in xrange(8):
            for y in xrange(16):
                self.clear_pixel(x,y)
#d=LedDisplay()
#d.draw_face()
#d.draw_image()

temp="""
0000000000000000
0000000000000000
0111011101110111
0000100000001000
0000100000001000
0000000000000000
0001110000011100
0000000000000000"""


#d.draw_image()
#d.draw_template(temp)
#d.draw_text('sleep.')
#d.clear_display()

