"""Website Queries."""
import flask
import website


def pagination(postid_lte, page, tagid=None):
    """Return a page with 20 earring posts, optionally filtered by tag."""
    size = 20  # 20 posts per page
    offset = page * size
    connection = website.model.get_db()
    if tagid:
        # Query when a tag is provided
        cur = connection.execute(
            """
            SELECT posts.postid, posts.filename, posts.name, posts.price, 
                   posts.description, posts.status, posts.created
            FROM posts
            JOIN post_tags ON posts.postid = post_tags.postid
            JOIN tags ON post_tags.tagid = tags.tagid
            WHERE posts.postid <= ? AND tags.tagid = ?
            ORDER BY posts.postid DESC
            LIMIT ? OFFSET ?;
            """,
            (postid_lte, tagid, size, offset)
        )
    else:
        # Query when no tag is provided
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


def get_all_tags():
    """Gets all tags."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT tags.tagid "
        "FROM tags "
    )
    all_tags = cur.fetchall()
    return all_tags


def get_tag_name(tagid):
    """Gets tag name from id."""
    connection = website.model.get_db()
    cur = connection.execute(
        "SELECT tags.name "
        "FROM tags "
        "WHERE tags.tagid = ?",
        (tagid,)
    )
    name = cur.fetchone()
    name = name["name"]  # get as string
    return name
