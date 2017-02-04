import os
from flask import Flask,request,session,g,redirect,url_for,abort,\
	render_template,flash

app=Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	SECRET_KEY='2cb01991546cb41ced2a37ddef4ab1ec2821ada450c56085',
	USERNAME='admin',
	PASSWORD='default',
))

@app.route('/')
def welcome():
    return render_template('welcome.html')

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
