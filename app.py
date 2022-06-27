from app import app
from app import db
from app.models import *

@app.route('/')
def index():
    return 'Rhaniel2!'


@app.before_first_request
def create_db():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)