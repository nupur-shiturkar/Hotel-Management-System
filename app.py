from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import os

app=Flask(__name__,template_folder='templates')

#MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()
mysql.init_app(app)




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET','POST'] )
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form['username']
        contact = request.form['contact']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accounts(username, contact, email, password) VALUES(%s, %s, %s, %s)", (username, contact, email, hash_password))
        mysql.connection.commit()
        session['username'] = username
        session['contact'] = contact
        session['email'] = email
        return redirect(url_for('home'))
    


@app.route('/login', methods = ['GET', 'POST'] )
def login():

    if request.method == 'POST' :
        
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        if email=='rutu@gmail.com' and password=='rutu@123'.encode('utf-8'):
            session['logged_in'] = True
            session['username'] = 'Rutuja'
            session['email'] = 'rutu@gmail.com'
            return redirect(url_for('admin'))
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM accounts WHERE email=%s", [email] )
        user = cur.fetchone()
        cur.close()
    
        if user is not None:
            
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['logged_in'] = True
                session['username'] = user['username']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else:
                 return "Invalid Login"

        else:
            return "Invalid Login"

    else:
        return render_template("login.html")
        
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/logout')
def logout():
        session.clear()
        return render_template('home.html')

 


if __name__ == "__main__":
    SECRET_KEY = os.urandom(24) 
    app.secret_key = SECRET_KEY
    app.run(debug=True)
