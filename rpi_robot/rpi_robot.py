import os
import time
from flask import Flask,request,session,g,redirect,url_for,abort,\
	render_template,flash,Response
from camera_rpi import Camera
from functools import wraps
import subprocess


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


@app.route('/control',methods=['GET','POST'])
@login_required
def control():
    
    if request.method=="POST":
        if request.form.get('start_video'):        
            
            #subprocess.Popen(['ffserver','-f','/etc/ffserver.conf'])
            subprocess.Popen(['/usr/sbin/webcam.sh'],shell=True)
        elif request.form.get('stop_video'):
               
             subprocess.call(['sudo','pkill','ffserver'])
  
    return render_template('control.html')

@app.route('/<pin>',methods=['POST'])
def reroute(pin):
    print 7777777,pin
    return redirect(url_for('control'))

def gen_thread(camera):
    print 66666
    global VIDEO_START
    print 99999,VIDEO_START
    while VIDEO_START:
        #print 1
        frame=camera.get_frame()
  
        yield(b'--frame\n'
               b'Content-Type: image\n\n'+frame+b'\n')
   
def gen(camera):
    print 3333
    thread=threading.Thread(target=gen_thread,args=(camera,))
    print thread
    thread.start()
    print 2,thread

@app.route('/video_feed')
def video_feed():
   
    return Response(gen_thread(Camera()),
            mimetype='multipart/x-mixed-replace;boundary=frame')


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
