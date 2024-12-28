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

@website.app.route("/posts/", methods=["POST"])
def update_posts():
    """Create, delete, or edit posts."""
    connection = website.model.get_db()
    operation = flask.request.form['operation']
    if operation == "create":
        name = flask.request.form['name']
        price = flask.request.form['price']
        description = flask.request.form['description']
        status = flask.request.form['status']

        # Get file object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        # Check if no file was uploaded or the file is empty
        if filename == "" or fileobj.read() == b"":
            return flask.abort(400)

        # Check if the file is empty without altering the file pointer
        fileobj.seek(0, os.SEEK_END)  # Move to the end of the file
        fileobj.seek(0)  # Reset pointer to the beginning

        # Compute base name (filename without directory) w UUID
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = website.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(path)

        connection.execute(
            "INSERT INTO posts (filename, name, price, description, "
            "status) VALUES (?, ?, ?, ?, ?)",
            (uuid_basename, name, price, description, status))
    # endif creating a post
    if operation == "delete":
        postid_to_delete = flask.request.form['postid']
        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE postid = ? ",
            (postid_to_delete,)
        )
        result = cur.fetchone()
        filename_to_delete = result['filename']  # gets file_to_delete as str
        connection.execute(
            "DELETE FROM posts WHERE postid = ?",
            (postid_to_delete,)
        )
        path = website.app.config["UPLOAD_FOLDER"] / filename_to_delete
        os.remove(path)
    # endif deleting a post
    # FIXME: write delete and edit
    url = flask.url_for('show_index')  # return to home page
    return flask.redirect(url)

