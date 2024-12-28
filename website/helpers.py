"""Helper functions to use throughout."""
import re

def string_to_url(string):
    """Convert a string to a URL-friendly format."""
    # Convert to lowercase
    string = string.lower()
    # Replace spaces and other non-alphanumeric characters with a single hyphen
    string = re.sub(r'[^a-z0-9]+', '-', string)
    # Remove trailing hyphens
    url = string.strip('-')
    return url


def url_to_string(url):
    """Convert a URL-friendly format back to a human-readable string."""
    # Replace hyphens with spaces
    string = url.replace('-', ' ')
    # Capitalize each word
    string = ' '.join(word.capitalize() for word in string.split())
    return string