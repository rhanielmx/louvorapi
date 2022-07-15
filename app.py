from app import app

@app.route('/')
def index():
    return 'Rhaniel2!'


if __name__ == "__main__":
    app.run(debug=True)