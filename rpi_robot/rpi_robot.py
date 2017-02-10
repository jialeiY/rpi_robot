

import os
import time
from flask import Flask,request,session,g,redirect,url_for,abort,\
	render_template,flash,Response
from camera_rpi import Camera
from functools import wraps
import subprocess
import motor

app=Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
	SECRET_KEY='2cb01991546cb41ced2a37ddef4ab1ec2821ada450c56085',
	USERNAME='admin',
	PASSWORD='default',
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
    print move
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

@app.route('/control',methods=['GET','POST'])
@login_required
def control():
    if request.method=="POST":
        
        print 1111,request
        print 2222,request.form
        if request.form.get('start_video'):        
            
            #subprocess.Popen(['ffserver','-f','/etc/ffserver.conf'])
            subprocess.Popen(['/usr/sbin/webcam.sh'],shell=True)
        elif request.form.get('stop_video'):
               
             subprocess.call(['sudo','pkill','ffserver'])
    return render_template('control.html')


@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!=app.config['USERNAME'] or \
               request.form['password']!=app.config['PASSWORD']:
            error='invalid username or password'
        else:
            session['logged_in']=True
            flash('you were logged in')
            return redirect(url_for('welcome'))
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('login'))


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=1)
