from flask import Blueprint, jsonify, request
from db import get_connection

students_bp = Blueprint('students', __name__)

# GET all students
@students_bp.route('/students', methods=['GET'])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return jsonify(students)

# POST add a new student
@students_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, email) VALUES (%s, %s)",
        (data['name'], data['email'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201