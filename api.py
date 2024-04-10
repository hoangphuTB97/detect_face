from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
db_file = 'database_new.db'

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYEES")
    rows = cursor.fetchall()
    conn.close()
    employees = []
    for row in rows:
        employee = {
            'id': row[0],
            'name': row[1],
            'gender': row[2],
            'birth_year': row[3],
            'position': row[4],
            'department': row[5]
        }
        employees.append(employee)
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYEES WHERE ID = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        employee = {
            'id': row[0],
            'name': row[1],
            'gender': row[2],
            'birth_year': row[3],
            'position': row[4],
            'department': row[5]
        }
        return jsonify(employee)
    else:
        return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)