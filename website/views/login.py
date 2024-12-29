"""
Website login view for owner.

URLs include:
/login
"""
import flask
from werkzeug.security import check_password_hash
import website


@website.app.route('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        # Check the submitted password
        password = flask.request.form.get('password')
        # Check if the password matches the stored hash
        if check_password_hash(website.app.config["OWNER_PASSWORD_HASH"],
                               password):
            flask.session['logged_in'] = True
            url = flask.url_for('show_index')  # return to home page
            return flask.redirect(url)
        else:
            error = "Incorrect password, please try again."
            return flask.render_template('login.html', error=error)

    # If it's a GET request, just show the login page
    return flask.render_template('login.html')