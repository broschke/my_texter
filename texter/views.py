from flask import render_template
from flask import request, redirect, url_for
from . import app
from .database import session
from flask import flash
from flask.ext.login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import User, Notification


@app.route("/")
def home():
    return render_template("base.html")

@app.route("/about")
def about():
    return render_template("about.html")
    
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("dashboard"))

@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")
    
@app.route("/register", methods=["POST"])
def register_post():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    
    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("register_post"))
    if len(password) < 8:
        flash("Password needs to be at least 8 characters", "danger")
        return redirect(url_for("register_post"))
    user = User(first_name=first_name, last_name=last_name,email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
    return redirect(url_for("home"))
    
@app.route("/dashboard")
@login_required
def dashboard():
    notifications = current_user.notifications
    contacts = current_user.contacts
    return render_template("dashboard.html",notifications=notifications, contacts=contacts)
    
@app.route("/notification/new")
@login_required
def new_notification():
    return render_template("new_notification.html")
    
@app.route("/notification/new", methods=["POST"])
@login_required
def new_notification_post():
    subject = request.form["subject"]
    timezone = request.form["timezone"]
    frequency = request.form["frequency"]
    days = request.form["days"]
    status = request.form["status"]
    user = current_user
    notification = Notification(
        subject = subject,
        timezone = timezone,
        frequency = frequency,
        days = days,
        status = status,
        user = user)
    session.add(notification)
    session.commit()
    #call twilio function here
    #enable or disable
    return redirect(url_for("dashboard"))
    
@app.route("/notification/<id>/edit")
@login_required
def edit_notification(id):
    notification = session.query(Notification)
    notification = notification.get(id)
    return render_template("edit_notification.html", notification = notification)
    #left side, notif variable on html file. right side, notif of query

@app.route("/notification/<id>/edit", methods=["POST"])
@login_required
def edit_notification_post(id):
    notification = session.query(Notification)
    notification = notification.get(id)
    notification.subject = request.form["subject"]
    notification.timezone = request.form["timezone"]
    notification.frequency = request.form["frequency"]
    notification.days = request.form["days"]
    notification.status = request.form["status"]
    session.commit()
    return redirect(url_for("dashboard"))

@app.route("/contacts")
@login_required
def contacts():
    return render_template("contacts.html")

@app.route("/contacts", methods=["POST"])
@login_required
def contacts_post():
    number1 = request.form["number1"]
    number2 = request.form["number2"]
    user = current_user
    contacts = Contact(
        number1 = number1,
        number2 = number2,
        user = user)
    session.add(contacts)    
    session.commit()
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
    
@app.route("/notification/<id>/delete", methods=["GET","POST"])
@login_required
def delete_notification(id):
    notification = session.query(Notification)
    notification = notification.get(id)
    session.delete(notification)
    session.commit()
    return redirect(url_for("dashboard"))

@app.route("/contacts/<id>/delete", methods=["GET","POST"])
@login_required
def delete_contact(id):
    contact = session.query(Contact)
    contact = contact.get(id)
    session.delete(contact)
    session.commit()
    return redirect(url_for("dashboard"))
    
