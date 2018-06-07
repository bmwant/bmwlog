from bottle import run
from app import app, config as conf


if __name__ == '__main__':
    if conf.DO_NOT_WRITE_BYTECODE:
        import sys
        sys.dont_write_bytecode = True  # without *.pyc files

    run(app=app, host=conf.RUN_HOST, port=conf.RUN_PORT,
        debug=conf.DEBUG, reloader=conf.RELOADER)
else:
    # for gunicorn launch
    app = app
