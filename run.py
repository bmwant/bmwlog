from bottle import run, default_app, debug
from app import app, config as conf

if __name__ == '__main__':
    import sys
    #sys.dont_write_bytecode = True  # without *.pyc files
    run(app=app, host=conf.RUN_HOST, port=conf.RUN_PORT,
        debug=conf.DEBUG, reloader=conf.RELOADER)
else:
    #for gunicorn launch
    app = default_app()
