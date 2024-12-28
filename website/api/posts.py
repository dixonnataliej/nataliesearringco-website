"""REST API for posts."""
import flask
import website
from website.api import queries
from website import helpers



@website.app.route('/api/v1/posts/')
def get_posts():
    """Get posts."""
    # Get arguments
    most_recent_postid = queries.get_recent_postid()
    postid_lte = flask.request.args.get("postid_lte",
                                        default=most_recent_postid, type=int)
    page = flask.request.args.get("page", default=0, type=int)

    if page < 0:
        flask.abort(400)
    size = 20
    # Get all relevant posts
    all_posts = queries.pagination(postid_lte, page)
    if all_posts is None:
        num_posts = 0
    else:
        num_posts = len(all_posts)
    # Update how many times we put a post into the response and the next url
    if num_posts < size:
        it_num = num_posts
        next = ""
    else:
        it_num = size
        next = "/api/v1/posts/?size=" + str(size) + "&page=" + str(
            page + 1) + "&postid_lte=" + str(postid_lte)

    # Dictionary to return
    posts_data = {
        "next": next,
    }
    # List of posts we're returning
    posts_dict = []
    for i in range(it_num):
        postid = all_posts[i]["postid"]
        url = "/api/v1/posts/" + str(postid) + "/"
        new_post = {"postid": postid, "url": url}
        posts_dict.append(new_post)

    # Add posts to return data
    posts_data["results"] = posts_dict
    path = flask.request.path
    query_string = flask.request.query_string.decode('utf-8')
    if query_string:
        url = path + "?" + query_string
    else:
        url = path
    posts_data["url"] = url

    return flask.jsonify(posts_data), 200


@website.app.route('/api/v1/posts/<int:postid>/')
def get_one_post(postid):
    """Get one post from post url."""

    # Check postid in range
    in_range = queries.postid_inrange(postid)
    if not in_range:
        return flask.abort(404)

    data = {}
    post_info = queries.get_post_info(postid)
    data["postid"] = postid
    data["img_url"] = "/uploads/" + post_info["filename"]
    data["name"] = post_info["name"]
    data["price"] = post_info["price"]
    data["description"] = post_info["description"]
    data["status"] = post_info["status"]
    data["created"] = post_info["created"]
    data["humanPostUrl"] = ("/posts/"
                            + helpers.string_to_url(post_info["name"]) + '/')

    # Fetch and add tags to the data
    tags = queries.get_tags_for_post(postid)
    data["tags"] = tags

    return flask.jsonify(data), 200
