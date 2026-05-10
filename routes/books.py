from flask import Blueprint, jsonify, request
from db import get_connection

books_bp = Blueprint('books', __name__)

# GET all books
@books_bp.route('/books', methods=['GET'])
def get_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

# POST add a new book
@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (isbn, title, author, total_copies, book_language, category_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (data['isbn'], data['title'], data['author'], data['total_copies'], data['book_language'], data['category_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully"}), 201