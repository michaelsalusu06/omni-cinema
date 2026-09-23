import os
import sqlite3
import subprocess
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')
DB_FILE = 'omnicinema.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        if os.path.exists('schema.sql'):
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/movies', methods=['GET'])
def get_movies():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return jsonify([dict(m) for m in movies])

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    schedules = conn.execute('''
        SELECT s.id, m.title, m.price, s.hall_number, s.showtime 
        FROM schedules s 
        JOIN movies m ON s.movie_id = m.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(s) for s in schedules])

@app.route('/api/seats', methods=['GET'])
def get_seats():
    schedule_id = request.args.get('schedule_id', 1)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    seats = conn.execute(
        "SELECT * FROM seats WHERE schedule_id = ? ORDER BY row_num, col_num", 
        (schedule_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(s) for s in seats])

@app.route('/api/buy-ticket', methods=['POST'])
def buy_ticket():
    data = request.json
    schedule_id = data.get('schedule_id', 1)
    row_num = data.get('row_num')
    col_num = data.get('col_num')
    age = data.get('age', 20)
    amount_paid = data.get('amount_paid', 0.0)

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    schedule_info = cursor.execute('''
        SELECT m.price FROM schedules s 
        JOIN movies m ON s.movie_id = m.id 
        WHERE s.id = ?
    ''', (schedule_id,)).fetchone()

    if not schedule_info:
        conn.close()
        return jsonify({"success": False, "message": "Invalid schedule selection."}), 400

    ticket_price = schedule_info['price']

    seat = cursor.execute(
        "SELECT is_booked FROM seats WHERE schedule_id = ? AND row_num = ? AND col_num = ?",
        (schedule_id, row_num, col_num)
    ).fetchone()

    if not seat:
        conn.close()
        return jsonify({"success": False, "message": "Seat does not exist."}), 404

    subprocess.run(["javac", "seats.java"], cwd=BASE_DIR)

    java_result = subprocess.run(
        ["java", "-cp", ".", "seats", str(row_num), str(col_num), str(seat['is_booked'])],
        capture_output=True, text=True, cwd=BASE_DIR
    )

    if java_result.returncode != 0:
        conn.close()
        return jsonify({"success": False, "message": "Java Engine: Seat is already booked!"}), 400

    cs_project = os.path.join(BASE_DIR, "payment-service", "PaymentService")
    cs_result = subprocess.run(
        ["dotnet", "run", "--project", cs_project, "--", str(ticket_price), str(age), str(amount_paid)],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    
    cs_stdout = cs_result.stdout.strip()
    cs_stderr = cs_result.stderr.strip()

    success_line = next((line for line in cs_stdout.splitlines() if "SUCCESS:" in line), None)

    if success_line:
        parts = success_line.split(":")
        final_price = float(parts[1])
        change = float(parts[2])

        row_letter = chr(64 + row_num)
        seat_name = f"{row_letter}{col_num}"

        cursor.execute(
            "UPDATE seats SET is_booked = 1 WHERE schedule_id = ? AND row_num = ? AND col_num = ?",
            (schedule_id, row_num, col_num)
        )
        cursor.execute(
            "INSERT INTO sales (schedule_id, customer_name, tickets_sold, seat_numbers, total_price, payment_type) VALUES (?, ?, ?, ?, ?, ?)",
            (schedule_id, "Customer", 1, seat_name, final_price, "Cash")
        )
        conn.commit()
        conn.close()

        return jsonify({
            "success": True, 
            "message": f"Successfully booked Seat {seat_name}!",
            "price": final_price,
            "change": change
        })
    else:
        conn.close()
        raw_msg = cs_stdout or cs_stderr or "Unknown C# execution response"
        return jsonify({"success": False, "message": f"C# Payment Service Output: {raw_msg}"}), 400

if __name__ == '__main__':
    init_db()
    print("OmniCinema system running at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)