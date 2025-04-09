from flask import Flask, render_template, request, jsonify
from config import get_db_connection  # import koneksi dari config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def data_handler():
    if request.method == 'GET':
        return jsonify({"message": "Hello from Flask API"})
    
    if request.method == 'POST':
        data = request.get_json()
        nama = data.get('nama')
        alamat = data.get('alamat')

        if not nama or not alamat:
            return jsonify({"error": "Nama dan alamat wajib diisi"}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (nama, alamat) VALUES (?, ?)", (nama, alamat))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Data berhasil disimpan dan koneksi sudah diletakan di file config.js!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
