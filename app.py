from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
import os
from ultralytics import YOLO
from config import get_db_connection  # import koneksi dari config
from Corest.test import get_data, insert_data
from Corest.yolo1 import detect_parfum 
from routes import API_DATA,API_BASE

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route(API_DATA, methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return get_data()
    elif request.method == 'POST':
        return insert_data()

@app.route(API_BASE+'/detect-parfum', methods=['POST'])
def yolo_detect_parfum():
    return detect_parfum()

@app.route('/detect-parfum-view', methods=['GET', 'POST'])
def detect_parfum_view():
    if request.method == 'POST':
        # Ambil file video dan referensi dari form
        video_file = request.files.get('video')
        reference_image_file = request.files.get('reference_image')

        if not video_file or not reference_image_file:
            return "Video dan gambar referensi wajib diunggah!", 400

        # Simpan file yang diunggah
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        reference_image_path = os.path.join(app.config['UPLOAD_FOLDER'], reference_image_file.filename)
        video_file.save(video_path)
        reference_image_file.save(reference_image_path)

        # Proses video
        output_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + video_file.filename)
        process_video(video_path, reference_image_path, output_video_path)

        # Redirect ke halaman hasil
        return redirect(url_for('view_result', video_filename='output_' + video_file.filename))

    return render_template('upload.html')

@app.route('/view-result/<video_filename>')
def view_result(video_filename):
    video_url = url_for('static', filename=f'uploads/{video_filename}')
    print(video_url)
    return render_template('result.html', video_url=video_url)

def process_video(video_path, reference_image_path, output_video_path):
    # Load model YOLO pre-trained
    model = YOLO('yolov8n.pt')

    # Load gambar referensi
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_COLOR)
    # Resize gambar referensi agar lebih kecil jika diperlukan
    reference_image = cv2.resize(reference_image, (100, 100))  # Sesuaikan ukuran (50x50 adalah contoh)
    reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Load video
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Gunakan codec H.264
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Deteksi objek dalam frame
        results = model(frame)

        # Konversi frame ke grayscale untuk pencocokan template
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Pencocokan template
        res = cv2.matchTemplate(frame_gray, reference_image_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.4  # Ambang batas kemiripan
        loc = np.where(res >= threshold)
        print("Pencocokan template selesai")
        print("loc:")
        print(loc)
        # Tandai objek yang cocok dengan kotak merah
        # for pt in zip(*loc[::-1]):
        #     print("Object sedang ditandai 1")
        #     cv2.rectangle(frame, (pt[0], pt[1]), (pt[0] + reference_image.shape[1], pt[1] + reference_image.shape[0]), (0, 0, 255), 2)
        # # Tandai objek yang cocok dengan titik hijau
        for pt in zip(*loc[::-1]):
            print("Object sedang ditandai 2")
            cv2.circle(frame, (pt[0] + reference_image.shape[1] // 2, pt[1] + reference_image.shape[0] // 2), 5, (0, 255, 0), -1)

        # Tulis frame ke video output
        out.write(frame)

    cap.release()
    out.release()

if __name__ == '__main__':
    app.run(debug=True)