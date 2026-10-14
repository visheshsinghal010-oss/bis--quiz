import os

port = os.environ.get("PORT", os.environ.get("APP_PORT", "10000"))
bind = f"0.0.0.0:{port}"
workers = 2
threads = 4
timeout = 120
accesslog = "-"
errorlog = "-"
