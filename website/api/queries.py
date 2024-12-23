"""Website Queries."""
import flask
import website


def pagination(postid_lte, page):
    """Return a page with 20 earring posts."""
    size = 20  # 20 posts per page
    offset = page * size
    connection = website.model.get_db()
    cur = connection.execute(
        """
        SELECT posts.postid, posts.filename, posts.name, posts.price, 
        posts.description, posts.status, posts.created
        FROM posts
        WHERE posts.postid <= ?
        ORDER BY posts.postid DESC
        LIMIT ? OFFSET ?;
        """,
        (postid_lte, size, offset)
    )
    posts = cur.fetchall()
    return posts


def get_recent_postid():
    """Get most recent postid."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "ORDER BY posts.postid DESC "
        "LIMIT 1;"
    )
    postid = cur.fetchone()
    postid = postid["postid"]
    return postid
