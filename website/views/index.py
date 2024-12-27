"""
Website index (main) view.

URLs include:
/
"""
import flask
import pathlib
import website


@website.app.route('/')
def show_index():
    """Display / route."""
    connection = website.model.get_db()

    cur = connection.execute(
        "SELECT name "
        "FROM posts"
    )
    post_names = cur.fetchall()

    context = {"post_names": post_names}
    return flask.render_template("index.html", **context)


@website.app.route('/uploads/<filename>')
def serve_image(filename):
    """Serves image."""
    upload_folder = website.app.config["UPLOAD_FOLDER"]
    file_path = pathlib.Path(upload_folder) / filename

    if not file_path.exists():
        return flask.abort(404)

    return flask.send_from_directory(website.app.config["UPLOAD_FOLDER"],
                                     filename)
