from flask import render_template, request, Blueprint, redirect, url_for
# from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import desc
from flaskr.model import User
from time import ctime


main = Blueprint('main', __name__)


@main.route("/")
def index():
    # start the journey from by login
    # return redirect(url_for("users.login"))
    return "HELLO"


@main.route("/home", methods=['GET', 'POST'])
# @login_required
def home():
    # get the current page, and put a default value of 1
    # current_page = request.args.get('current_page', 1, type=int)
    # posts = Post.query.order_by(desc(Post.date)).paginate(page=current_page, per_page=6)
    # return render_template("home.html", posts=posts, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                        datetime=datetime, current_user=current_user, time=ctime())
    return render_template("base.html")