from flask import Flask, render_template, request, jsonify
from config import get_db_connection  # import koneksi dari config
from Corest.test import get_data,insert_data
from  routes import API_DATA
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route(API_DATA, methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return get_data()
    elif request.method == 'POST':
        return insert_data()

if __name__ == '__main__':
    app.run(debug=True)