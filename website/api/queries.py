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

def postid_inrange(postid):
    """Check if postid is in range of existing ids."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )
    details = cur.fetchone()
    if details is None:
        return False
    else:
        return True

def get_post_info(postid):
    """Gets post info."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT postid, filename, name, price, description, status, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )
    post_info = cur.fetchone()
    return post_info

def get_tags_for_post(postid):
    """Gets tags for a post."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT tags.name "
        "FROM tags "
        "INNER JOIN post_tags ON tags.tagid = post_tags.tagid "
        "WHERE post_tags.postid = ?",
        (postid,)
    )
    tags = cur.fetchall()
    return [tag["name"] for tag in tags]