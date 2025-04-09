from flask import jsonify,request
from config import get_db_connection



def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, alamat FROM Users")
        rows = cursor.fetchall()
        result = [{"id": row.id, "nama": row.nama, "alamat": row.alamat} for row in rows]
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def insert_data():
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