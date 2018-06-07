import os

from bottle import static_file

from app import app, config


# serving static files
root = os.path.expanduser(config.ROOT_FOLDER)


@app.route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root=root)


@app.route('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root=root)
