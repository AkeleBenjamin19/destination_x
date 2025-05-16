# run.py

from dotenv import load_dotenv
load_dotenv()

# import the factory, *not* the package
from app import create_app

# this *is* your Flask application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
