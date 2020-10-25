from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_wtf import Form
import os



app=Flask(__name__,template_folder='templates')

#MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_management'

mysql = MySQL()
mysql.init_app(app)




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'] )
def register():
    
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
