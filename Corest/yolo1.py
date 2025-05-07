from flask import jsonify,request
from config import get_db_connection
import cv2
from ultralytics import YOLO
import numpy as np

def detect_parfum():
    """
    Endpoint untuk mendeteksi botol parfum dalam video dan menggantinya dengan gambar botol parfum.
    """
    video_file = request.files.get('video')
    replacement_image_file = request.files.get('replacement_image')

    if not video_file or not replacement_image_file:
        return jsonify({"error": "Video file dan replacement image file wajib diisi"}), 400

    # Simpan video sementara
    video_path = "temp_video.mp4"
    video_file.save(video_path)

    # Simpan gambar botol parfum sementara
    replacement_image_path = "temp_replacement_image.png"
    replacement_image_file.save(replacement_image_path)

    # Load model YOLO pre-trained
    model = YOLO('yolov8n.pt')  # Gunakan model YOLO pre-trained

    # Load video dan gambar botol parfum
    cap = cv2.VideoCapture(video_path)
    replacement_image = cv2.imread(replacement_image_path, cv2.IMREAD_UNCHANGED)

    # Fungsi untuk overlay gambar
    def overlay_image(background, overlay, x, y, w, h):
        overlay_resized = cv2.resize(overlay, (w, h))
        alpha = overlay_resized[:, :, 3] / 255.0  # Ambil channel alpha
        for c in range(0, 3):  # Untuk setiap channel warna (B, G, R)
            background[y:y+h, x:x+w, c] = (
                alpha * overlay_resized[:, :, c] + (1 - alpha) * background[y:y+h, x:x+w, c]
            )
        return background

    # Simpan video hasil
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    # Loop untuk membaca setiap frame video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Deteksi objek dalam frame
        results = model(frame)

        # Loop melalui semua objek yang terdeteksi
        for box in results[0].boxes:  # Akses bounding boxes dari hasil deteksi
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Koordinat bounding box
            conf = box.conf[0]  # Confidence score
            if conf > 0.5:  # Hanya gunakan deteksi dengan confidence > 50%
                w, h = x2 - x1, y2 - y1
                frame = overlay_image(frame, replacement_image, x1, y1, w, h)

        # Tulis frame ke video output
        out.write(frame)

    cap.release()
    out.release()

    return jsonify({"message": "Video berhasil diproses!", "output_video": "output_video.mp4"}), 200
