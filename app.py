from flask import Flask, render_template, request, redirect, session, flash
from Database import User, SessionLocal, hash_password, verify_password
from sqlalchemy.orm import Session
import os
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    db: Session = SessionLocal()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.hashed_password):
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            return redirect('/')
        else:
            flash('Invalid credentials', 'error')
            return redirect('/login')
    return render_template('index.html')


@app.route('/SignUp', methods=['POST'])
def signup():
    db: Session = SessionLocal()
    full_name = request.form['full_name']
    shop_name = request.form['shop_name']
    email = request.form['email']
    password = request.form['password']

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        flash("Email already exists", "error")
        return redirect('/login')

    user = User(
        full_name=full_name,
        email=email,
        shop_name=shop_name,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    flash("Signup successful. Please login.")
    return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('profile.html')


@app.route('/management')
def management():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('management.html')


@app.context_processor
def inject_user():
    return dict(user_name=session.get('user_name', ''))


if __name__ == '__main__':
    # os.makedirs("templates", exist_ok=True)
    # shutil.copy("index.html", "templates/index.html")
    # shutil.copy("loginpage.html", "templates/loginpage.html")
    # shutil.copy("profile.html", "templates/profile.html")
    # shutil.copy("management.html", "templates/management.html")
    app.run(debug=True)
