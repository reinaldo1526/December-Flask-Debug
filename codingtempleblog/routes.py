from codingtempleblog import app, db
from flask import render_template, request, flash, redirect, url_for

# Import of Forms
from codingtempleblog.forms import SignUpForm, LoginForm, PostForm, PaymentForm

# Import Models
from codingtempleblog.models import User,Post

# Import Flask-Login Module/functions
from flask_login import login_user, current_user,logout_user, login_required
from werkzeug.security import check_password_hash

# Home Route
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html",post = posts)

@app.route("/register",methods=["GET","POST"])
def createUser():
    signupForm = SignUpForm()
    if request .method == 'POST':
        flash("Thanks for Signing Up!")
        # Gathering Form Data
        username = signupForm.username.data
        email = signupForm.email.data
        password = signupForm.password.data
        print(username,email,password )

        # Add Form data to User Model Class
        user = User(username, email, password)
        db.session.add(user) # Start communication with Database
        db.session.commit() # Save Data to Database
        return redirect(url_for('login'))
    else:
        flash("Your form is missing some data")
    return render_template('register.html',signupform = signupForm)

@app.route('/login',methods=["GET","POST"])
def login():
    loginForm = LoginForm()
    if request.method == "POST":
        user_email = loginForm.email.data
        password = loginForm.password.data
        logged_user = User.query.filter(User.email == user_email).first()
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            print(current_user.username)
            return redirect(url_for('home'))
    else:
        print("Not valid")
    return render_template('login.html',loginform = loginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/post',methods=["GET","POST"])
@login_required
def post():
    postForm = PostForm()
    title = postForm.title.data
    content = postForm.content.data
    user_id = current_user.id
    print(title, content,user_id)

    # Instatiate Post Class
    post = Post(title = title, content = content, user_id = user_id)
    db.session.add(post)
    db.session.commit()
    return render_template('post.html',postform = postForm)


