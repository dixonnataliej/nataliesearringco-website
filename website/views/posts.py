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


@website.app.route('/posts/<postname_url_slug>/')  # might change posts to
# products
def show_post(postname_url_slug):
    """Display post."""
    # Connect to database
    connection = website.model.get_db()
    name = helpers.url_to_string(postname_url_slug)

    cur = connection.execute(
        "SELECT postid, filename, name, price, description, status, created "
        "FROM posts "
        "WHERE name = ?",
        (name,)
    )
    post_info = cur.fetchone()
    postid = post_info["postid"]
    img_url = "/uploads/" + post_info["filename"]
    price = post_info["price"]
    description = post_info["description"]
    status = post_info["status"]
    created_arrow = arrow.get(post_info["created"])
    timestamp = created_arrow.humanize()

    context = {"postid": postid, "img_url": img_url, "name": name, "price":
        price, "description": description, "status": status, "timestamp":
        timestamp}
    return flask.render_template("post.html", **context)
