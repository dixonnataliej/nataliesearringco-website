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

LOGGER = flask.logging.create_logger(website.app)

@website.app.route('/posts/<postname_url_slug>/<postid_url_slug>/')
# might change posts to products
def show_post(postname_url_slug, postid_url_slug):
    """Display post."""
    logged_in = flask.session.get('logged_in')

    # Connect to database
    connection = website.model.get_db()

    cur = connection.execute(
        "SELECT filename, name, price, description, status, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid_url_slug,)
    )
    post_info = cur.fetchone()
    postid = postid_url_slug
    img_url = "/uploads/" + post_info["filename"]
    name = post_info["name"]
    price = post_info["price"]
    description = post_info["description"]
    status = post_info["status"]
    created_arrow = arrow.get(post_info["created"])
    timestamp = created_arrow.humanize()

    cur = connection.execute(
        "SELECT name, tagid "
        "FROM tags"
    )
    all_tags = cur.fetchall()

    # Fetch tags already linked to the post
    post_tags_ids = connection.execute(
        "SELECT tagid FROM post_tags WHERE postid = ?", (postid,)
    ).fetchall()

    # Convert `post_tags` to a list of tag IDs for easier checking
    post_tags_ids = [tag['tagid'] for tag in post_tags_ids]

    context = {"postid": postid, "img_url": img_url, "name": name, "price":
        price, "description": description, "status": status, "timestamp":
        timestamp, "postname_url_slug": postname_url_slug, "all_tags":
        all_tags, "post_tags_ids": post_tags_ids, "logged_in": logged_in}
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

        cur = connection.execute(
            "INSERT INTO posts (filename, name, price, description, "
            "status) VALUES (?, ?, ?, ?, ?)",
            (uuid_basename, name, price, description, status))
        postid = cur.lastrowid  # gets new post id

        # Tags
        selected_tags = flask.request.form.getlist("tags")  # List of tagids
        new_tags = flask.request.form.getlist("new_tags[]")  # List of new tags

        # Link selected tags to the new post
        for tagid in selected_tags:
            link_tag_to_post(postid, tagid)

        LOGGER.debug(new_tags)

        # Handle new tags if provided
        for new_tag in new_tags:
            if new_tag.strip():  # Ignore empty inputs
                new_tag_id = create_new_tag(
                    new_tag.strip())  # Save each new tag
                link_tag_to_post(postid, new_tag_id)
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

        # Remove links to tags
        post_tags = connection.execute(
            "SELECT tagid FROM post_tags WHERE postid = ?", (postid_to_delete,)
        ).fetchall()
        post_tags = [tag['tagid'] for tag in post_tags]
        for tagid in post_tags:
            unlink_tag_to_post(postid_to_delete, tagid)
    # endif deleting a post

    if operation == "edit":
        name = flask.request.form['name']
        price = flask.request.form['price']
        description = flask.request.form['description']
        status = flask.request.form['status']
        postid = flask.request.form['postid']
        connection.execute(
            "UPDATE posts SET name = ?, price = ?, description = ?, "
            "status = ? WHERE postid = ?",
            (name, price, description, status, postid,)
        )  # update all with new or previous content, perhaps inefficient

        # Get optional file object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename

        # Check if a file was uploaded
        if not filename == "":
            if fileobj.read() == b"":
                return flask.abort(400)  # if fileobj is empty
            # find cur filename to delete
            cur = connection.execute(
                "SELECT filename "
                "FROM posts "
                "WHERE postid = ?",
                (postid,)
            )
            file_to_delete = cur.fetchone()
            filename_to_delete = file_to_delete['filename']
            path = website.app.config["UPLOAD_FOLDER"] / filename_to_delete
            os.remove(path)

            # Check if the file is empty without altering the file pointer
            fileobj.seek(0, os.SEEK_END)  # Move to the end of the file
            fileobj.seek(0)  # Reset pointer to the beginning

            # Compute base name (filename without directory) w UUID
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"
            connection.execute(
                "UPDATE posts SET filename = ? WHERE postid = ?",
                (uuid_basename, postid,)
            )
            # Save to disk
            path = website.app.config["UPLOAD_FOLDER"] / uuid_basename
            fileobj.save(path)
        # endif uploaded a new file
        # now deal with tags
        selected_tags = flask.request.form.getlist('tags')
        selected_tags = [int(tagid) for tagid in
                         selected_tags]  # Convert to integers
        # Existing tags
        post_tags = connection.execute(
            "SELECT tagid FROM post_tags WHERE postid = ?", (postid,)
        ).fetchall()
        post_tags = [tag['tagid'] for tag in post_tags]
        # Tags to add
        tags_to_add = set(selected_tags) - set(post_tags)
        for tagid in tags_to_add:
            link_tag_to_post(postid, tagid)

        # Tags to remove
        tags_to_remove = set(post_tags) - set(selected_tags)
        for tagid in tags_to_remove:
            unlink_tag_to_post(postid, tagid)

        url = flask.request.args.get(
            'target',
            default=flask.url_for('show_index'),
            type=str
        )  # redirect to post's page
        return flask.redirect(url)
        # end if edit
    url = flask.url_for('show_index')  # return to home page
    return flask.redirect(url)


def link_tag_to_post(postid, tagid):
    """Link tag to post by inserting into post-tags table."""
    connection = website.model.get_db()
    connection.execute(
        "INSERT INTO post_tags (postid, tagid) "
        "VALUES (?, ?) ",
        (postid, tagid, )
    )
    return


def create_new_tag(tag_name):
    """Create new tag and insert into tags table and return tag id."""
    connection = website.model.get_db()
    cur = connection.execute(
        "INSERT INTO tags (name) "
        "VALUES (?) ",
        (tag_name, )
    )
    new_tag_id = cur.lastrowid
    return new_tag_id


def unlink_tag_to_post(postid, tagid):
    """Delete a post tag connection"""
    connection = website.model.get_db()
    connection.execute(
        "DELETE FROM post_tags "
        "WHERE postid = ? AND "
        "tagid = ?",
        (postid, tagid)
        )
    return
