
from flask import Flask,render_template,request,redirect,session,flash,url_for
from flask import Flask, render_template, Response
from functools import wraps
from flask_mysqldb import MySQL
import cv2


app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='2525'
app.config['MYSQL_DB']='db_sample'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)
 
#Login
@app.route('/') 
@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from users where EMAIL=%s and UPASS=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["UNAME"]
            session['email']=data["EMAIL"]

            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")
  
#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  
#Registration  
@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("insert into users(UNAME,UPASS,EMAIL) values(%s,%s,%s)",(name,pwd,email))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template("reg.html",status=status)
    
camera = cv2.VideoCapture(0)  # use 0 for web camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


#Home page
@app.route("/home")
@is_logged_in
def home():
    
	return render_template('home.html')
    # import the opencv library


#Camera page
@app.route("/cam")
@is_logged_in
def cam():
    
	return render_template('cam.html')
    # import the opencv library


# define a video capture object

    
#logout
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))
    
if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)