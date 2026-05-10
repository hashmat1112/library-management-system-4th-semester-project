from flask import Flask
from routes.books import books_bp
from routes.students import students_bp
from routes.issued_books import issued_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(books_bp)
app.register_blueprint(students_bp)
app.register_blueprint(issued_bp)

# Home route
@app.route("/")
def home():
    return {
        "message": "Library Management System API",
        "status": "running",
        "endpoints": {
            "books":    "/books",
            "students": "/students",
            "issued":   "/issued",
            "issue":    "/issue",
            "return":   "/return",
            "queue":    "/queue"
        }
    }

if __name__ == "__main__":
    app.run(debug=False)
