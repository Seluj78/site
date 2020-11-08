import json

from docutils.core import publish_parts
from docutils.writers import html5_polyglot
from flask import abort
from flask import Blueprint
from flask import render_template
from peewee import DoesNotExist

from afpy.models.NewsEntry import NewsEntry
from afpy.static import AFPY_ROOT

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home_page():
    all_news = NewsEntry.select()
    return render_template("pages/index.html", body_id="index", posts=all_news)


@home_bp.route("/communaute")
def community_page():
    with open(f"{AFPY_ROOT}/afpy/data/meetups.json", "r") as handle:
        meetups = json.load(handle)
    return render_template("pages/communaute.html", body_id="communaute", meetups=meetups)


@home_bp.route("/adherer")
def adhere_page():
    return render_template("pages/adhesions.html", body_id="adhesions")


@home_bp.route("/discussion")
def discussion_page():
    return render_template("pages/discussion.html", body_id="discussion")


@home_bp.route("/docs/<name>")
def render_rest(name):
    try:
        with open(f"{AFPY_ROOT}/afpy/templates/rest/{name}.rst") as fd:
            parts = publish_parts(
                source=fd.read(), writer=html5_polyglot.Writer(), settings_overrides={"initial_header_level": 2}
            )
    except FileNotFoundError:
        abort(404)
    return render_template("pages/rst.html", body_id=name, html=parts["body"], title=parts["title"])


@home_bp.route("/posts/<id>")
def post_render(id: int):
    try:
        post = NewsEntry.get_by_id(id)
    except DoesNotExist:
        abort(404)
    return render_template("pages/post.html", body_id="post", post=post, name=post.title)
