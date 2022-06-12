from flask import Flask, render_template, request, redirect, session, flash, url_for, Response
from functools import wraps
from flask_mysqldb import MySQL
from subprocess import call
import cv2
import torch
import mysql.connector
import numpy
from playsound import playsound

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2525'
app.config['MYSQL_DB'] = 'wd_cctv'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
app.secret_key = 'dont tell anyone'

# Login

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        u_name = request.form["u_name"]
        u_password = request.form["u_password"]
        cur = mysql.connection.cursor()
        cur.execute(
            "select * from user where u_name=%s and u_password=%s", (u_name, u_password))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True

            session['username'] = data["u_name"]
            session['email'] = data["u_email"]
            session['phone'] = data["u_phone"]

            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("login.html")

# check if user logged in

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

# View
@app.route('/user/view', methods=['POST', 'GET'])
@is_logged_in
def check_products_url():
    cur = mysql.connection.cursor()
    cur.execute("select * from user")
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    #if error=="":
    return render_template("/user/view.html", user=data)
    #else:
      #  return render_template("ViewUser.html", result=error)

#Edit User
@app.route('/user/edit/<u_id>', methods = ['POST', 'GET'])
@is_logged_in
def get_employee(u_id):
    cur = mysql.connection.cursor()
    cur.execute('select * from user WHERE u_id = %s', [u_id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('/user/edit.html', user = data[0])
 
@app.route('/user/update/<u_id>', methods=['POST'])
@is_logged_in
def update_employee(u_id):
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['email']
        upass = request.form['upass']
        phone = request.form['phone']
        shift = request.form['shift']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE user SET u_name = %s, u_password = %s, u_email = %s, u_phone = %s, u_shift = %s WHERE u_id = %s """, (name, upass, email, phone, shift, u_id))
        flash('user Updated Successfully')
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("select * from user")
        mysql.connection.commit()
        data = cur.fetchall()
        cur.close()
    return render_template('/user/view.html',user=data)

@app.route('/delete/<int:u_id>', methods = ['POST','GET'])
def delete_employee(u_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE u_id = {0}'.format(u_id))
    mysql.connection.commit()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("select * from user")
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    flash('User Removed Successfully')
    return render_template('/user/view.html',user=data)

# Add User
@app.route('/user/add', methods=['POST', 'GET'])
@is_logged_in
def AddUser():
    status = False
    if request.method == 'POST':
        uname = request.form["uname"]
        upass = request.form["upass"]
        email = request.form["email"]
        phone = request.form["phone"]
        shift = request.form["shift"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT into user values(null,%s,%s,%s,%s,%s,0)",
                    (uname, upass, email, phone, shift,))
        mysql.connection.commit()
        cur.close()
        flash('Adding User Successfully.', 'success')
       
    return render_template("/user/add.html", status=status)

# Camera
camera = cv2.VideoCapture(0)  # use 0 for web camera
# for local webcam use cv2.VideoCapture(0)
def gen_frames():
    model = torch.hub.load(r'C:\Users\moco_\Documents\Python\GP2\GP2_files',
                           'custom',
                           path=r'best.pt',
                           source='local')  # local repo
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            image = frame
            results = model(image)
            results.xyxy[0]
            x = results.pandas().xyxy[0]  # or .show(), .save(), .crop(), .pandas(), etc.
            rows = x.shape[0]
            cols = x.shape[1]

            for i in range(rows):

                ob_class = str(x.iat[i, cols - 2])
                ob_name = str(x.iat[i, cols - 1])
                ob_conf = str(x.iat[i, cols - 3])
                x1 = int(x.iat[i, cols - 7])
                y1 = int(x.iat[i, cols - 6])
                x2 = int(x.iat[i, cols - 5])
                y2 = int(x.iat[i, cols - 4])

                start_point = (x1, y1)  # represents the top left corner of rectangle
                end_point = (x2, y2)  # represents the bottom right corner of rectangle
                if int(ob_class) == 0:
                    color = (180, 0, 0)  # Blue color in BGR
                elif int(ob_class) == 1:
                    color = (0, 0, 180)  # Red color in BGR
                thickness = 2  # Line thickness of 2 px

                label = (ob_name.title() + " " + "{:.2%}".format(float(ob_conf)))

                # Draw a rectangle with blue line borders of thickness of 2 px
                frame = cv2.rectangle(image, start_point, end_point, color, thickness)

                # For the text background
                # Finds space required by the text so that we can put a background with that amount of width.
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

                # Prints the text.
                img = cv2.rectangle(image, (x1, y1 - 20), (x1 + w, y1), color, -1)
                img = cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

                # For printing text
                img = cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                frame = image

                if float(ob_conf) > 0.6:
                    playsound('Police.mp3')

                print(ob_class, ob_name, ob_conf)

                with app.app_context():
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT into object values(null,%s,%s,%s,CURRENT_DATE(),CURRENT_TIME)",
                                (ob_class, ob_name, ob_conf,))
                    mysql.connection.commit()
                    cur.close()

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Home page
@app.route("/home")
@is_logged_in
def home():
    return render_template('home.html')
    # import the opencv library


# Camera page
@app.route("/cam")
@is_logged_in
def cam():
    return render_template('cam.html')


# logout
@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

