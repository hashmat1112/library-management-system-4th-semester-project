from flask import Blueprint, jsonify, request
from db import get_connection
from datetime import date, timedelta

issued_bp = Blueprint('issued', __name__)

# GET all issued books
@issued_bp.route('/issued', methods=['GET'])
def get_issued():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.issue_id, s.name as student, b.title as book,
               i.issue_date, i.due_date, i.return_date, i.status
        FROM issued_books i
        JOIN students s ON i.student_id = s.student_id
        JOIN books b ON i.book_id = b.book_id
    """)
    issued = cursor.fetchall()
    conn.close()
    return jsonify(issued)

# POST issue a book to a student
@issued_bp.route('/issue', methods=['POST'])
def issue_book():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # check available copies
    cursor.execute("SELECT total_copies FROM books WHERE book_id = %s", (data['book_id'],))
    book = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as issued_count FROM issued_books WHERE book_id = %s AND status = 'issued'", (data['book_id'],))
    count = cursor.fetchone()

    available = book['total_copies'] - count['issued_count']

    if available <= 0:
        conn.close()
        return jsonify({"message": "No copies available. Student added to waiting queue."}), 400

    # issue the book
    due_date = date.today() + timedelta(days=14)
    cursor.execute(
        "INSERT INTO issued_books (book_id, student_id, due_date) VALUES (%s, %s, %s)",
        (data['book_id'], data['student_id'], due_date)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Book issued successfully", "due_date": str(due_date)}), 201

# POST return a book
@issued_bp.route('/return', methods=['POST'])
def return_book():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE issued_books SET status = 'returned', return_date = CURDATE() WHERE issue_id = %s",
        (data['issue_id'],)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Book returned successfully"}), 200

# GET waiting queue
@issued_bp.route('/queue', methods=['GET'])
def get_queue():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT w.queue_id, s.name as student, b.title as book, w.requested_at
        FROM waiting_queue w
        JOIN students s ON w.student_id = s.student_id
        JOIN books b ON w.book_id = b.book_id
        ORDER BY w.requested_at ASC
    """)
    queue = cursor.fetchall()
    conn.close()
    return jsonify(queue)

# POST add to waiting queue
@issued_bp.route('/queue', methods=['POST'])
def add_to_queue():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO waiting_queue (book_id, student_id) VALUES (%s, %s)",
        (data['book_id'], data['student_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Added to waiting queue successfully"}), 201