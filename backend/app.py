import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS  

# Fungsi untuk membuat koneksi ke database PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",  # Sesuaikan dengan nama database yang Anda buat
        user="ical",      # Sesuaikan dengan nama user
        password="123"  # Sesuaikan dengan password user
    )
    return conn

# Inisialisasi aplikasi Flask
app = Flask(__name__)
# Mengaktifkan CORS untuk semua domain
CORS(app)  # Ini memungkinkan API diakses dari domain yang berbeda (frontend)

# Route utama - hanya mengembalikan pesan sederhana
@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# Endpoint untuk membaca semua data dari tabel 'items' (READ operation)
@app.route('/api/items', methods=['GET'])
def get_items():

    # Membuat koneksi ke database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Eksekusi query SELECT untuk mengambil semua item
    cur.execute("SELECT id, name, description FROM items;")
    rows = cur.fetchall()  # Mengambil semua hasil query
    
    # Menutup cursor dan koneksi untuk menghindari memory leak
    cur.close()
    conn.close()
    
    # Mengubah hasil query menjadi format JSON yang lebih mudah dibaca frontend
    items = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
    return jsonify(items)

# Endpoint untuk menambahkan data baru ke tabel 'items' (CREATE operation)
@app.route('/api/items', methods=['POST'])
def create_item():
    
    # Mengambil data JSON dari request
    data = request.json
    name = data['name']
    description = data['description']
    
    # Membuat koneksi ke database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Eksekusi query INSERT dan dapatkan ID yang baru dibuat
    cur.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;", 
                (name, description))
    new_id = cur.fetchone()[0]  # Mengambil ID yang baru dibuat
    
    # Commit perubahan ke database
    conn.commit()
    
    # Menutup cursor dan koneksi
    cur.close()
    conn.close()
    
    # Mengembalikan item yang baru dibuat dengan status 201 (Created)
    return jsonify({"id": new_id, "name": name, "description": description}), 201

# Endpoint untuk mengupdate data yang ada di tabel 'items' (UPDATE operation)
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    
    # Mengambil data JSON dari request
    data = request.json
    name = data['name']
    description = data['description']
    
    # Membuat koneksi ke database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Eksekusi query UPDATE dan cek apakah ada baris yang terpengaruh
    cur.execute("UPDATE items SET name = %s, description = %s WHERE id = %s RETURNING id;", 
                (name, description, id))
    
    # Cek apakah item dengan ID tersebut ada
    # rowcount akan bernilai 0 jika tidak ada baris yang diupdate
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    # Commit perubahan ke database
    conn.commit()
    
    # Menutup cursor dan koneksi
    cur.close()
    conn.close()
    
    # Mengembalikan item yang sudah diupdate
    return jsonify({"id": id, "name": name, "description": description})

# Endpoint untuk menghapus data dari tabel 'items' (DELETE operation)
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    
    # Membuat koneksi ke database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Cek terlebih dahulu apakah item dengan ID tersebut ada
    cur.execute("SELECT id FROM items WHERE id = %s;", (id,))
    if cur.fetchone() is None:
        # Jika tidak ada hasil, berarti item tidak ditemukan
        cur.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    # Eksekusi query DELETE untuk menghapus item
    cur.execute("DELETE FROM items WHERE id = %s;", (id,))
    
    # Commit perubahan ke database
    conn.commit()
    
    # Menutup cursor dan koneksi
    cur.close()
    conn.close()
    
    # Mengembalikan pesan sukses
    return jsonify({"message": f"Item with id {id} has been deleted"}), 200

# Endpoint tambahan untuk demonstrasi
@app.route('/api/data')
def get_data():
    return jsonify({"data": "Hello from Flask API"})

# Blok utama untuk menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)