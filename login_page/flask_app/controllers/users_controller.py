from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/login.html')

@app.route("/create_user" ,methods=['post'])
def create_user():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    if User.login_user(request.form):
        flash('email is already in use or your password and confirm password do not match')
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
}
    session["user_id"] = User.create_user(data)
    return redirect('/home')

@app.route("/login_user" ,methods=['post'])
def login():
    user_db = User.login_user(request.form)
    if not user_db: 
        flash("Invalid email address!!!")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash('Email/ Password is invalid')
        return redirect('/login')
    session["user_id"] = user_db.id
    return redirect('/home')

@app.route("/home")
def home():
    return render_template ("home.html", user = User.get_one_user({"user_id":session["user_id"]}))

if __name__ =="__main__":
    app.run(debug=True, port=5001)