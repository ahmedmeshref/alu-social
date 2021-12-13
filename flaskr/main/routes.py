from typing import final
from flask import render_template, request, Blueprint, redirect, url_for, flash, jsonify, abort
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from sqlalchemy import desc
from flaskr.model import User, Major, Campus, Event, Job
from flaskr import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash


main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.get("/")
def index():
    return render_template("index.html")


@main.get("/home")
# @login_required
def home():
    # get the current page, and put a default value of 1
    events = Event.query.order_by(desc(Event.date)).all()
    return render_template("show_events.html", events=events)


@main.get("/mentors")
def view_mentors():
    user = User.query.all()
    return render_template("mentors.html", users=user, active='mentor')


@main.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    hash_password = generate_password_hash(password, method="sha256")
    if User.query.filter_by(email=email).first():
        flash("Account with the same email already exists.", "danger")
        return redirect(url_for("main.index"))
    user = User(username=name, email=email, password=hash_password,
                group_id=2, major_id=1, campus_id=1)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    return redirect(url_for("main.home"))


@main.post("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        return redirect(url_for("main.home"))
    flash("Invalid Credentials! Please try again.", "danger")
    return redirect(url_for("main.index"))


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authorized to access the content!", "danger")
    logout_user()
    return redirect(url_for("main.login"))


@main.post("/events/add")
@login_required
def new_event():
    title = request.get_json()['title']
    description = request.get_json()['description']
    date = datetime.strptime(request.get_json()['date'], '20%y-%m-%d')

    try:
        event = Event(title=title, content=description,
                      author=current_user, date=date)
        db.session.add(event)
        db.session.commit()
        return jsonify({
            'id': event.id,
            'title': event.title,
            'description': event.content,
            'date': event.date,
            'username': event.author.username,
            'author_id': event.author.id
        })
    except:
        db.rollback()
        flash("Couldn't add event", "danger")


@main.route("/events")
def show_events():
    events = Event.query.order_by(desc(Event.date)).all()
    return render_template('show_events.html', events=events, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, active='events')


def validate_event(event_id):
    # check if post exists or not
    event = Event.query.get_or_404(event_id)
    # check if current user is the author or the current user is an admin and the author is an end user
    if (event.author == current_user):
        return event
    abort(403)


@main.route("/events/delete", methods=['POST'])
@login_required
def delete_post():
    event_id = request.get_json()['event_id']
    event = validate_event(event_id)
    data = jsonify({
        'event_id': event.id,
        'title': event.title
    })
    db.session.delete(event)
    db.session.commit()
    return data



@main.route("/jobs")
def show_jobs():
    jobs = Job.query.order_by(desc(Job.deadline)).all()
    return render_template('show_jobs.html', jobs=jobs, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, active='jobs')
