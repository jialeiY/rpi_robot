

import os
import time
from flask import Flask,request,session,g,redirect,url_for,abort,\
	render_template,flash,Response
from camera_rpi import Camera
from functools import wraps
import subprocess
import motor
import led
from passlib.hash import pbkdf2_sha256

app=Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
	SECRET_KEY='2cb01991546cb41ced2a37ddef4ab1ec2821ada450c56085',
	USERNAME='',
	PASSWORD='',
))

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
   
        if not session.get('logged_in'):
            return redirect(url_for('login',next=request.url))
        return f(*args,**kwargs)
    return decorated_function


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/control/cam',methods=['POST'])
@login_required
def move_cam():
    motor_cam=motor.ControlCameraMotors()
    move=request.form.get('move')
    if move=='forward':
        motor_cam.forward()
    elif move=="backward":
        motor_cam.backward()
    else:
        return 'error'
    return 'success'

@app.route('/control/mv',methods=['POST'])
@login_required
def move_robot():
    motor_mv=motor.ControlMoveMotors()
    move=request.form.get('move')
    #print move
    if move=='left':
        motor_mv.turn_left()
    elif move=='right':
        motor_mv.turn_right()
    elif move=='forward':
        motor_mv.forward()
    elif move=='backward':
        motor_mv.backward()
    else:
        return 'error'
    return 'success'        



@app.route('/control/led',methods=['POST'])
@login_required
def led_matrix():
    led_display=led.LedDisplay()
    data=request.form
    if data.get('type')=='stop_led':
        led_display.stop_led()
    elif data.get('type')=='text_display':
        led_display.draw_text(data.get('data'))
    elif data.get('type')=='temp_display':
        led_display.draw_template(data.get('data'))
    elif data.get('type')=='emoji_display':
        led_display.draw_emoji(img=data.get('data'))
    else:
        return error
    return 'success'        


LED_TEMPLATE="""
0000000000000000
0000000000000000
0111011101110111
0000100000001000
0000100000001000
0000000000000000
0001110000011100
0000000000000000"""

def load_led_images():
    dir_path=os.path.dirname(os.path.realpath(__file__))
    relative_path="/static/img/emoji"
    emoji_path=dir_path+relative_path
    emoji_list=[os.path.join(relative_path,im) for im in os.listdir(emoji_path)]
   
    return emoji_list

@app.route('/control',methods=['GET','POST'])
@login_required
def control():
    emoji_list=load_led_images()
    if request.method=="POST":
        
        if request.form.get('start_video'):        
            
            #subprocess.Popen(['ffserver','-f','/etc/ffserver.conf'])
            subprocess.Popen(['/usr/sbin/webcam.sh'],shell=True)
        elif request.form.get('stop_video'):
               
             subprocess.call(['sudo','pkill','ffserver'])

        elif request.form.get('reboot'):
            subprocess.call(['sudo','reboot'])
        else:
            return 'error'
    return render_template('control.html',
                    led_template=LED_TEMPLATE,emoji=emoji_list)


@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        #print 1111,request.form
        if pbkdf2_sha256.verify(request.form['username'],app.config['USERNAME']) and \
               pbkdf2_sha256.verify(request.form['password'],app.config['PASSWORD']):
            session['logged_in']=True
            flash('you were logged in')
            return redirect(url_for('welcome'))
        else:
            error='invalid username or password'
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('login'))


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=1)
