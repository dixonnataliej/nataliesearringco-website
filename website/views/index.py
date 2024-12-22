"""
Website index (main) view.

URLs include:
/
"""
import flask
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