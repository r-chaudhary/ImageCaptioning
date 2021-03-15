from flask import render_template, url_for, flash, redirect, request, session
from flask.helpers import make_response
from flask_mysqldb import MySQLdb
from FlaskApp import app, mysql, dropzone
from FlaskApp.forms import RegistrationForm, LoginForm
from functools import wraps
import os


@app.route('/cookie_set')
def cookie_set(home_func):
    @wraps(home_func)
    def wrapper(*args, **kwargs):
        logged_in = request.cookies.get("logged_in")
        if logged_in: 
            return home_func(*args, **kwargs)
        else:
            response = make_response(redirect(url_for('home')))
            response.set_cookie('logged_in', 'False')
            return response
    
    return wrapper


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@cookie_set
def home():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

    return render_template("home.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        # DB Procedure
        cursor = mysql.connection.cursor()
        cmd = f"select * from USER where username='{username}' AND password='{password}'"
        cursor.execute(cmd)
        account = cursor.fetchone()
        print(account)

        # Verification and Cookie
        if account:
            flash('You have been loged in','success')
            response = make_response(redirect(url_for('home')))
            response.set_cookie('username', username)
            response.set_cookie('fullname', account[3])
            response.set_cookie('logged_in', 'True')
            return response
        else:
            flash('Login Failed , Please check username/password','danger')
            response = make_response(redirect(url_for('login')))
            response.set_cookie('logged_in', 'False')
            return response

    # Default Template           
    return render_template("login.html", form=form)



@app.route("/logout")
def logout():
    flash('You have been Loged out','success')
    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', 'None')
    response.set_cookie('logged_in', 'False')
    return response



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cmd = f"INSERT INTO USER(USERNAME,PASSWORD,FULLNAME,EMAIL) VALUES('{form.username.data}','{form.password.data}','{form.fullname.data}','{form.email.data}')"
        print(cmd)
        try:
            cursor.execute(cmd)
            cursor.execute('commit')
            cursor.close()
            flash(f'Account Created for {form.username.data}', 'success')
            session['logged_in'] = True
            session['username'] = form.username.data
            return redirect(url_for('home'))            
        except (MySQLdb.Error) as e:
            if e.args[0] == 1062:
                flash('Username already exists!','danger')
    
    return render_template("register.html", form=form)










@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join('UPLOADED_PATH', f.filename))

    return 'upload template'



@app.route("/about")
def about():
    return render_template("about.html")



@app.route('/completed')
def completed():
    return '<h1>The Redirected Page</h1><p>Upload completed.</p>'



@app.route("/example")
def example():
    return render_template("example.html")



@app.route("/crowdsource")
def crowdsource():
    return render_template("crowdsource.html")



@app.route("/profile")
def account():
    return "User account"
