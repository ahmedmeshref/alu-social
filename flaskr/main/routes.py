from os import major
from threading import active_count
from typing import final
from flask import render_template, request, Blueprint, redirect, url_for, flash, jsonify, abort
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from sqlalchemy import desc
from flaskr.model import Group, User, Major, Campus, Event, Job
from flaskr import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash


main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.get("/")
def index():
    majors = Major.query.all()
    campuses = Campus.query.all()
    groups = Group.query.all()
    return render_template("index.html", groups=groups, majors=majors, campuses=campuses)


@main.get("/home")
@login_required
def home():
    # get the current page, and put a default value of 1
    events = Event.query.order_by(desc(Event.date)).all()
    return render_template("show_events.html", events=events)


@main.get("/mentors")
@login_required
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
    group_id = request.form.get("group")
    major_id = request.form.get("major")
    campus_id = request.form.get("campus")
    hash_password = generate_password_hash(password, method="sha256")
    if User.query.filter_by(email=email).first():
        flash("Account with the same email already exists.", "danger")
        return redirect(url_for("main.index"))
    try:
        user = User(username=name, email=email, password=hash_password,
                    group_id=int(group_id), major_id=int(major_id), campus_id=int(campus_id))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        return redirect(url_for("main.home"))
    except:
        flash("Invalid singup attempt.", "danger")
        return redirect(url_for("main.index"))


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
@login_required
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
@login_required
def show_jobs():
    jobs = Job.query.order_by(desc(Job.deadline)).all()
    return render_template('show_jobs.html', jobs=jobs, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), active='jobs')


@main.post("/jobs/add")
@login_required
def new_job():
    title = request.get_json()['title']
    description = request.get_json()['description']
    app_link = request.get_json()['application_link']
    deadline = datetime.strptime(request.get_json()['deadline'], '20%y-%m-%d')
    print(title, app_link)

    try:
        job = Job(title=title, content=description,
                  author=current_user, deadline=deadline, application_link=app_link)
        print(job)
        db.session.add(job)
        db.session.commit()
        return jsonify({
            'id': job.id,
            'title': job.title,
            'description': job.content,
            'deadline': job.deadline,
            'application_link': job.application_link,
            'username': job.author.username,
            'author_id': job.author.id
        })
    except:
        db.rollback()
        flash("Couldn't add job", "danger")

def validate_job(job_id):
    # check if post exists or not
    job = Job.query.get_or_404(job_id)
    # check if current user is the author or the current user is an admin and the author is an end user
    if job.author == current_user:
        return job
    abort(403)

@main.route("/jobs/delete", methods=['POST'])
@login_required
def delete_job():
    job_id = request.get_json()['job_id']
    job = validate_job(job_id)
    data = jsonify({
        'job_id': job.id,
        'title': job.title
    })
    db.session.delete(job)
    db.session.commit()
    return data


@main.get("/profile/<user_id>")
@login_required
def profile(user_id):
    # check if profile with the provided id exists
    user = User.query.get_or_404(user_id)
    # get the user posted events
    events = Event.query.filter_by(author=user).order_by(desc(Event.date)).all()
    return render_template("profile.html", title=f"profile - {user.username}", events=events,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime=datetime, user=user, active='profile')

@main.get("/chat")
@login_required
def chat():
    return render_template("chat.html", active='chat')


@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authorized to access the content!", "danger")
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/profile/update", methods=['POST', 'GET'])
@login_required
def update_profile():
    # check if the given user_id exist
    user = current_user
    if request.method == 'POST':
        username = request.form.get("username")
        group_id = request.form.get("group")
        major_id = request.form.get("major")
        campus_id = request.form.get("campus")
        user.username = username
        user.group_id = int(group_id)
        user.major_id=int(major_id)
        user.campus_id=int(campus_id)
        db.session.commit()
        return redirect('/home')

    majors = Major.query.all()
    campuses = Campus.query.all()
    groups = Group.query.all()
    return render_template("update_profile.html", title="Update Profile", majors=majors, campuses=campuses, groups=groups)
