"""REST API for tags."""
import flask
import website
from website.api import queries

LOGGER = flask.logging.create_logger(website.app)

@website.app.route('/api/v1/tags/')
def get_tags():
    """Get tags."""

    all_tags = queries.get_all_tags()
    num_tags = len(all_tags)
    tags_dict = []
    for i in range(num_tags):
        tagid = all_tags[i]["tagid"]
        url = "/api/v1/tags/" + str(tagid) + "/"
        new_tag = {"tagid": tagid, "url": url}
        tags_dict.append(new_tag)
    return flask.jsonify(tags_dict), 200


@website.app.route('/api/v1/tags/<int:tagid>/')
def get_one_tag(tagid):
    """Get one tag from tag url."""

    data = {"tagid": tagid, "name": queries.get_tag_name(tagid)}
    LOGGER.debug(data)
    return flask.jsonify(data), 200
