import psycopg2
from flask import Flask, jsonify, request

# Fungsi untuk koneksi ke database PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",  # Sesuaikan dengan nama database yang Anda buat
        user="ical",      # Sesuaikan dengan nama user
        password="123"  # Sesuaikan dengan password user
    )
    return conn

# Inisialisasi Flask
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# Endpoint untuk membaca data dari tabel 'items'
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM items;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    items = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
    return jsonify(items)

# Endpoint untuk menambahkan data ke tabel 'items'
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    name = data['name']
    description = data['description']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;", (name, description))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "name": name, "description": description}), 201

# Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)