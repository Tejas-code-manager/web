from flask import Flask, render_template,flash,request, redirect,session,url_for
from flask_mysqldb import MySQL
import hashlib
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(27)

# Configure db
db = json.load(open('db.json'))
app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['pass']
app.config['MYSQL_DB'] = db['mysqldb']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        email1 =hashlib.md5(email.encode())
        email2 = email1.hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email2))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'ids' in session:
        cur = mysql.connection.cursor()
        user4 = session['ids']
        getname = cur.execute("SELECT * FROM users WHERE id='{}'".format(user4))
        get2 = cur.fetchall()
        username = get2[0][1]
        # print(username)
        return render_template('dashboard.html',user5 =username)
    else:
        return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'ids' in session:
        return redirect('/dashboard')
    elif 'idsr' in session:
        return redirect('/adminer')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            pass1 = hashlib.md5(password.encode())
            pass2 = pass1.hexdigest()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email= '{}' AND password = '{}'".format(email, pass2))
            log = cur.fetchall()
            if len(log) > 0:
                session['ids'] = log[0][0]
                # print(session['ids'])
                return redirect('/dashboard')
            cur.execute("SELECT * FROM admin WHERE email= '{}' AND password = '{}'".format(email, pass2))
            log2 = cur.fetchall()
            if len(log2) > 0:
                session['idsr'] = log2[0][0]
                # print(session['ids'])
                return redirect('/adminer')
            else:
                return redirect('/login')

        return render_template('login.html')

@app.route('/adminer',methods=['GET','POST'])
def adminer():
    if 'idsr' in session:
        cur = mysql.connection.cursor()
        user7 = session['idsr']
        getname = cur.execute("SELECT * FROM admin WHERE id='{}'".format(user7))
        get4 = cur.fetchall()
        username1 = get4[0][1]
        # print(username)
        return render_template('test.html',user8 = username1)
    else:
        return redirect('/login')

@app.route('/addcourse',methods=['GET','POST'])
def dash():
    if 'idsr' in session:
        cur = mysql.connection.cursor()
        user7 = session['idsr']
        getname = cur.execute("SELECT * FROM admin WHERE id='{}'".format(user7))
        get4 = cur.fetchall()
        username1 = get4[0][1]
        return render_template('test2.html',user8 = username1)
    else:
        return redirect('/login')

@app.route('/addsnippets',methods=['GET','POST'])
def snippets():
    if 'idsr' in session:
        cur = mysql.connection.cursor()
        user7 = session['idsr']
        getname = cur.execute("SELECT * FROM admin WHERE id='{}'".format(user7))
        get4 = cur.fetchall()
        username1 = get4[0][1]
        return render_template('test2.html',user8 = username1)
    else:
        return redirect('/login')

@app.route('/addadmin',methods=['GET','POST'])
def addadmin():
    if 'idsr' in session:
        cur = mysql.connection.cursor()
        user7 = session['idsr']
        getname = cur.execute("SELECT * FROM admin WHERE id='{}'".format(user7))
        get4 = cur.fetchall()
        username1 = get4[0][1]
        return render_template('test2.html',user8 = username1)
    else:
        return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        pass1 = hashlib.md5(password.encode())
        pass2 = pass1.hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email ='{}'".format(email))
        log2 = cur.fetchall()
        if len(log2) > 0:
            return 'Email already exits'
        else:
            cur.execute("INSERT INTO users(name,email,password) VALUES('{}', '{}','{}')".format(name,email,pass2))
            mysql.connection.commit()
            cur.close()
            # session['ids'] = log[0][1]
            return redirect('/login')
    return render_template('register.html')

@app.route("/profile1", methods=['GET','POST'])
def profile1():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password')
        pass1 = hashlib.md5(password1.encode())
        pass2 = pass1.hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email ='{}'".format(email))
        log2 = cur.fetchall()
        if len(log2) > 0:
            return 'Email already exits'
        else:
            cur.execute("INSERT INTO users(name,email,password) VALUES('{}', '{}','{}')".format(name,email,pass2))
            mysql.connection.commit()
            cur.close()
            # session['ids'] = log[0][1]
            return redirect(url_for('/login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    if 'ids' in session:
        session.pop('ids')
    else:
        session.pop('idsr')
    return redirect('/login')

@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('test.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'ids' in session:
        idss = session['ids']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id ='{}'".format(idss))
        log5 = cur.fetchall()
        usern = log5[0][1]
        if request.method == 'POST':
            name = request.form.get('name')
            # email = request.form.get('email')
            # password2 = request.form.get('password')
            phone = request.form.get('phone')
            address = request.form.get('address')
            # pass3 = hashlib.md5(password2.encode())
            # pass4 = pass3.hexdigest()
            cur.execute("UPDATE users SET name='{}',phone='{}',address='{}' WHERE id ='{}'".format(name,phone,address,idss))
            mysql.connection.commit()
            cur.close()
            success = 'Your profile is successfully updated!'
            case1= True
            return redirect("/profile")
        else:
            success = 'Your details are never get stolen!'
            case1 = False
        return render_template('profile.html', emailer=idss, user5=usern, det=log5,green=success,case2 = case1)
    else:
        return redirect('/login')



@app.route('/test2', methods=['GET','POST'])
def test2():
    return render_template('layout.html')



if __name__ == '__main__':
    app.run(debug=True)
