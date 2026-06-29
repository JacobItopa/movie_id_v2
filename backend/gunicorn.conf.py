# Gunicorn configuration file
import os
import multiprocessing

# Bind to the port provided by Render
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Number of worker processes
workers = 4

# Use Uvicorn workers for FastAPI
worker_class = "uvicorn.workers.UvicornWorker"

# Massive timeout to allow for slow video downloads and AI processing
timeout = 300 # 5 minutes

# Maximum number of pending connections
backlog = 2048
