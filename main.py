# This file is used by Render's default start command (gunicorn main:app)
from backend.app import app

if __name__ == "__main__":
    app.run()
