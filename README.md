# Cloud-Computing


# Modul Praktikum 02 - Membuat API Sederhana dengan Flask


1. Masuk ke folder backend:
   ```bash
   cd cloud-project/backend
   ```
2. Membuat virtual environment:

    ```bash
    python -m venv venv
    ```

3. Aktivasi virtual environment:

    Untuk Windows:
    ```bash
    venv\Scripts\activate
    ```

4. Menginstal Flask
Instal Flask:
    ```bash
    pip install Flask
    ```


5. Menjalankan Aplikasi Flask
Jalankan aplikasi Flask:
    ```bash
    python app.py
    ```
6. Akses aplikasi flash di browser
    ```bash
    http://127.0.0.1:5000/
    http://localhost:5000/
    ```

# Modul Praktikum 03 - Membuat Aplikasi Frontend Sederhana dengan React + Vite

1. Berpindah ke direktori Frontend serta membuat proyek React baru dengan perintah
    ```bash
    cd frontend
    npm create vite@latest my-react-app -- --template react
    ```

2. Menjalankan React dan Vite menggunakan perintah
    ```bash
    npm run dev
    ```    

3. Membuat halaman sederhana pada src/App dengan code
    ```bash
    import React from 'react';

    function App() {
    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <h1>Hello from React + Vite!</h1>
        <p>This is a simple React app built with Vite.</p>
        </div>
    );
    }

    export default App;
    ```


# Modul Praktikum 04 - Menghubungkan React ke Flask

1. Mengaktifkan virtual environment menggunakan perintah
    ```bash
    .\venv\Scripts\activate 
    ```

2. Menambahkan Endpoint pada file app.py
    ```bash
    @app.route('/api/data')
    def get_data():
    return jsonify({"data": "Hello from Flask API"})
    ```

3. Menjalankan server Flask menggunakkan perintah
    ```bash
    app.py
    ```
    dan mengaksesnya di url
    ```bash
    http://localhost:5000/api/data.
    ```

4. Memanggil endpoint dari react pada file App.jsx
    ```bash
    import React, { useState, useEffect } from 'react';

    function App() {
    const [apiData, setApiData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:5000/api/data')
        .then(response => response.json())
        .then(data => {
            setApiData(data.data);
        })
        .catch(error => console.error(error));
    }, []);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <h1>React & Flask Integration</h1>
        <p>{apiData ? apiData : "Loading data..."}</p>
        </div>
    );
    }

    export default App;
    ```

5. Menjalankan terminal React menggunakan perintah
    ```bash
    npm run dev
    ```
    dan dapat diakses pada url
    ```bash
    http://localhost:5173/
    ```


# Modul Praktikum 05 - Integrasi Flask dengan PostgreSQL

1. Masuk kedalam virtual environment proyek Flask
    ```bash
    .\venv\Scripts\activate
    ```

2. Menginstall Psycopg2 dengan perintah
    ```bash
    pip install psycopg2
    ```
3. jika ada masalah gunakan perintah
    ```
    pip install psycopg2-binary
    ```
5. Melakukan verifikasi instalasi menggunakan perintah
    ```bash
    pip show psycopg2-binary
    ```
6. Membuat Koneksi database di PostgreSQL di file app.py, pastikan mengubah database sesuai dengan databasse kalian, begutupun dengan username dan password
    ```bash
    import psycopg2

    # Tambahkan di bagian atas file sebelum deklarasi route
    def get_db_connection():
        conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="student",
            password="password"
        )
        return conn

    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/')
    def home():
        return jsonify({"message": "Hello from Flask!"})

    @app.route('/api/data')
    def get_data():
        return jsonify({"data": "Hello from Flask API"})

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
    ```
7. Membuka pgAdmin lalu Masuk menggunakan user postgres atau user yang Anda buat sebelumnya.
8. - Klik kanan pada menu Databases → pilih Create → Database.
    - Isi nama database, misalnya test_db, dan simpan.
9. Membuat tabel melalui psql atau pgAdmin menggunakan perintah
    ```bash
    CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
    );
    ```
10. Menambahkan fungsi CRUD pada file app.py
    ```bash
    from flask import request

    @app.route('/api/items', methods=['GET'])
    def get_items():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        items = []
        for row in rows:
            items.append({"id": row[0], "name": row[1], "description": row[2]})
        return jsonify(items)

    @app.route('/api/items', methods=['POST'])
    def create_item():
        data = request.json
        name = data['name']
        description = data['description']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;",
                    (name, description))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": new_id, "name": name, "description": description}), 201
    ```
11. Jalankan flask menggunakan perintah
    ```bash
    python app.py
    ```
12. Cek endpoint menggunakan POSTMAN atau curl dengan perintah dibawah ini 
    ```bash
        # GET
    curl http://localhost:5000/api/items

    # POST
    curl -X POST -H "Content-Type: application/json" \
        -d '{"name": "Test Item", "description": "Test Description"}' \
        http://localhost:5000/api/items
    ```
13. Error handling
- Jika terjadi error saat menginstall 'psycopg2-binary', 
    ```
    Pastikan Python Versi Stabil (3.11.x atau 3.10.x), 
    ```
    ```
    tambahkan Path PostgreSQL ke Environment     Variables: Tambahkan lokasi file libpq.dll (biasanya C:\Program Files\PostgreSQL\<versi>\bin) ke sistem PATH.  
    ```
- jika terjadi error InsufficientPrivilege: permission denied for table items, gunakan perintah berikut
    ```bash
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO student;
    ```
- jika terjadi Connection Refused, lakukan verifikasi pgAdmin dengan perintah
    ```
    pg_ctl status
    ```
- jika GET Endpoint Kosong maka gunakan endpoint POST untuk menambahkan data
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "Item A", "description": "Deskripsi Item A"}' \
    http://localhost:5000/api/items
    ```

<br><br>

# Modul Praktikum 06 - Dockerization Bagian 1 (Membuat Dockerfile untuk Flask)

1. menjalankan perintah 
    ```bash
    docker info
    ```

- jika menghasilkan error seperti :
    ```bash
    Server:
    ERROR: error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.47/info": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
    ```
2.  buka aplikasi Docker Desktop dan tunggu hingga status "Docker is running" muncul.

3. Buatlah file dockerfile pada folder backend, isikan kode dibawah ini pada file dockerfile
    ```
    # backend/Dockerfile
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000
    CMD ["python", "app.py"]
    ```

4. Tambahkan kode dibawah ini pada file requirements.txt
    ```
    flask
    flask-cors
    psycopg2-binary
    ```

5. jalankan perintah dibawah ini untuk membangun image docker
    ```bash
    cd backend
    docker build -t flask-backend:1.0 .
    ```
6. jalankan container menggunakan perintah
    ```bash
    docker run -d -p 5000:5000 --name flask-container flask-backend:1.0
    ```
7. Cek aplikasi Flask berjalan di browser pada alamat
    ```bash
    http://localhost:5000.
    ```