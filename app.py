from flask import Flask, render_template, redirect, url_for, session, request, logging, flash
from flask_mysqldb import MySQL, MySQLdb
from flask_socketio import SocketIO, emit
import bcrypt
import os
from data import plots
# plots()

app=Flask(__name__,template_folder='templates')
app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'

#MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()
mysql.init_app(app)


socketio = SocketIO( app )

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from single_ac")
    sac = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from single_non_ac")
    snac = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from double_ac")
    dac = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from double_non_ac")
    dnac = cur.fetchall()
    cur.close()
    return render_template('home.html',sac=sac,snac=snac,dac=dac,dnac=dnac)
    


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
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin WHERE email=%s", [email])
        admin = cur.fetchone()
        if admin is not None :
            if password==admin['password']:
                session['logged_in'] = True
                session['username'] = admin['name']
                session['email'] = admin['email']
                return redirect(url_for('home'))
            else:
                return "Invalid Login"
            
            

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM accounts WHERE email=%s", [email] )
        user = cur.fetchone()
        cur.close()
        password=password.encode('utf-8')
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

@app.route('/book', methods=['GET','POST'] )
def book():
    if request.method == 'POST' :
        room_no = request.form['room_no']
        room_type = request.form['room_type']
        holder_name = request.form['holder_name']
        holder_mobile = request.form['holder_mobile']
        holder_address = request.form['holder_address']
        child_no = request.form['child_no']
        adult_no = request.form['adult_no']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        # status=1
        cur = mysql.connection.cursor()
        if room_type=='single_ac':
            cur.execute("Update single_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=1 where room_no=%s",(holder_name,holder_mobile,holder_address,child_no,adult_no,check_in_date,check_out_date,room_no))
        elif room_type=='single_non_ac':
            cur.execute("Update single_non_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=1 where room_no=%s",(holder_name,holder_mobile,holder_address,child_no,adult_no,check_in_date,check_out_date,room_no))
        elif room_type=='double_ac':
            cur.execute("Update double_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=1 where room_no=%s",(holder_name,holder_mobile,holder_address,child_no,adult_no,check_in_date,check_out_date,room_no))
        else:
            cur.execute("Update double_non_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=1 where room_no=%s",(holder_name,holder_mobile,holder_address,child_no,adult_no,check_in_date,check_out_date,room_no))
        cur.execute("INSERT INTO bookings(name, email, room_no, room_type) VALUES(%s, %s, %s, %s)",(holder_name,session['email'],room_no,room_type))
        # cur.execute("Update single_ac set holder_name=%s where room_no=%s",(holder_name,room_no))
        mysql.connection.commit()
        return redirect(url_for('home'))
 
@app.route('/cancel', methods=['GET','POST'] )
def cancel():
    if request.method == 'POST' :
        cur = mysql.connection.cursor()
        email=request.form['email']
        room=request.form['room-no']
        cur.execute("SELECT * FROM bookings WHERE email=%s and room_no=%s", (email,room))
        user = cur.fetchone()
        if user is not None:
            if user['room_type']=='single_ac':   
                cur.execute("Update single_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=0 where room_no=%s",(None,None,None,0,0,None,None,user['room_no']))           
            elif user['room_type']=='single_non_ac':
                cur.execute("Update single_non_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=0 where room_no=%s",(None,None,None,0,0,None,None,user['room_no']))            
            elif user['room_type']=='double_ac':
                cur.execute("Update double_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=0 where room_no=%s",(None,None,None,0,0,None,None,user['room_no']))
            else:
                cur.execute("Update double_non_ac set holder_name=%s,holder_mobile=%s,holder_address=%s,child=%s,adult=%s,in_date=%s,out_date=%s,status=0 where room_no=%s",(None,None,None,0,0,None,None,user['room_no']))
            cur.execute("Delete from bookings where email=%s and room_no=%s", (email,room))
            mysql.connection.commit()   
            return redirect(url_for('home'))    
        else:
            return "No bookings yet."
        cur.close()
        
    if request.method == 'GET' :
        return render_template('cancel.html')

@app.route('/chat', methods = ['GET', 'POST'] )
def chat():
    return render_template( './ChatApp.html' )

def messageRecived():
  print( 'message was received!!!' ) 

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == "__main__":
    SECRET_KEY = os.urandom(24) 
    app.secret_key = SECRET_KEY
    # app.run(port=9999,debug=True)
    socketio.run( app, debug = True )
