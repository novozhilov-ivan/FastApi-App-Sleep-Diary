import os

from app import app

if __name__ == "__main__":
    app.run(
        host=os.getenv('FLASK_HOST'),
        port=os.getenv('FLASK_PORT')
    )
