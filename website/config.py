"""Website development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'O\x85\xfc8\xb1>\xa9\xcd\xedUn\xd5\x87\xe5lQ#M\x0bq[\x0e9\xc4'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
WEBSITE_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = WEBSITE_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/website.sqlite3
DATABASE_FILENAME = WEBSITE_ROOT/'var'/'website.sqlite3'