"""Website package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (website/config.py)
app.config.from_object('website.config')

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import website.api  # noqa: E402  pylint: disable=wrong-import-position
import website.views  # noqa: E402  pylint: disable=wrong-import-position
import website.model  # noqa: E402  pylint: disable=wrong-import-position
