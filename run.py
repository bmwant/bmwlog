from bottle import run
from app import app


if __name__ == "__main__":
    run(app=app, 
        host='localhost', port=8081, debug=True, reloader=True)
