from functools import wraps
from flask import request, abort

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == 'db1Hp-1Ad2sP-0tl0II-8xh8s7-aaGk8':
            return view_function(*args, **kwargs)
        else:
            return "401"
    return decorated_function