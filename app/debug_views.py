import os

from bottle import static_file

from app import app, config
from app.helpers import render_template


# serving static files
root = os.path.expanduser(config.ROOT_FOLDER)


@app.route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root=root)


@app.route('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root=root)


@app.get('/502')
def test502():
    return render_template('errors/502.html')


@app.get('/500')
def test500():
    return render_template('errors/500.html')
