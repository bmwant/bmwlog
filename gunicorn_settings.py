bind = '127.0.0.1:8031'  # match to nginx settings file
workers = 1
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'