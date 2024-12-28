"""
Website individual post view.

URLs include:
/posts/<postname_url_slug>
"""
import pathlib
import uuid
import os
import re
import flask
import arrow
import website
from website import helpers


@website.app.route('/new_post/')
def show_new_post_page():
    """Display new post creation page."""
    context = {}
    return flask.render_template("new_post.html", **context)
