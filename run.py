from bottle import run, default_app, debug
from app import app, config as conf

if __name__ == '__main__':
    run(app=app, host=conf.RUN_HOST, port=conf.RUN_PORT,
        debug=conf.DEBUG, reloader=conf.RELOADER)
else:
    debug(True)
    import sys
    sys.dont_write_bytecode = True
    application = default_app()
