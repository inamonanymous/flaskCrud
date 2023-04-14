import sys
sys.path.append(r"C:\Users\Stephen Aguilar\Appdata\local\packages\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\localcache\local-packages\python310\site-packages")

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "many random bytes"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)

@app.route("/addStudents", methods=["POST"])
def addStudents():
    return render_template('add-students.html')

@app.route("/adding", methods=["POST"])
def adding():
    #if "back" in request.form:
    #    return redirect(url_for('index'))
        
    studName, studEmail, studPhone = request.form.get("name"), request.form.get("email"), request.form.get("phone")
    if len(studName) and len(studEmail) and len(studPhone) is None:
        return render_template('error.html')
    
    if not studPhone.isdigit():
        return render_template('error.html')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (studName, studEmail, studPhone))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

