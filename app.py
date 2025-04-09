from flask import Flask, render_template, request, jsonify
import pyodbc

app = Flask(__name__)
# Database COnnections
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=db_belajar;'
        'Trusted_Connection=yes;'
        'UID=sa;PWD=12345678;'

    )
    return conn
# Method API
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
            return jsonify({"message": "Data berhasil disimpan!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


