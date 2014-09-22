import os
from bottle import run, default_app
from app import app, config as conf

if __name__ == "__main__":
    run(app=app, 
        host=conf.RUN_HOST, port=conf.RUN_PORT, debug=conf.DEBUG, reloader=conf.RELOADER)
else:
	application = default_app()
