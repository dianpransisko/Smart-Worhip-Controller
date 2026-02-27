import cv2
import mediapipe as mp
import pygame
import os
import numpy as np

# ==============================
# 1. INISIALISASI
# ==============================
pygame.mixer.init()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

last_action = "netral"
stable_action = "netral"
pose_counter = 0
required_frames = 6  # pose harus stabil 6 frame

# ==============================
# 2. KONFIGURASI GRAFIK
# ==============================
labels = ["VERSE", "VERSE2", "CHORUS", "BRIDGE", "NETRAL"]
bar_width = 300
bar_height = 40
chart_width = 450
chart_height = len(labels) * 70 + 50

print("--- SISTEM MUSIK POSE PINTAR FINAL AKTIF ---")

# ==============================
# 3. LOOP UTAMA
# ==============================
while True:
    ret, frame = camera.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    current_action = "netral"

    # Default score grafik
    scores = {label.lower(): 0 for label in labels}
    scores["netral"] = 1.0

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        # Koordinat utama
        nose_y = landmarks[mp_pose.PoseLandmark.NOSE].y
        right_wrist_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y
        left_wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
        right_wrist_x = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x
        left_shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x

        # ==============================
        # 4. LOGIKA POSE (DENGAN MARGIN)
        # ==============================
        margin_y = 0.07
        margin_x = 0.08

        # CHORUS (dua tangan jelas di atas)
        if right_wrist_y < nose_y - margin_y and left_wrist_y < nose_y - margin_y:
            current_action = "chorus"

        # VERSE (kanan atas, kiri bawah jelas)
        elif right_wrist_y < nose_y - margin_y and left_wrist_y > nose_y + margin_y:
            current_action = "verse"

        # VERSE2 (kiri atas, kanan bawah jelas)
        elif left_wrist_y < nose_y - margin_y and right_wrist_y > nose_y + margin_y:
            current_action = "verse2"

        # BRIDGE (tangan kanan benar-benar menyilang badan)
        elif (right_wrist_x < left_shoulder_x - margin_x and
              abs(right_wrist_y - nose_y) < 0.25):
            current_action = "bridge"

        # Update grafik
        scores["netral"] = 0
        scores[current_action] = 1.0

    # ==============================
    # 5. STABILIZER (ANTI FLICKER)
    # ==============================
    if current_action == stable_action:
        pose_counter += 1
    else:
        pose_counter = 0
        stable_action = current_action

    # ==============================
    # 6. AUDIO EKSEKUSI
    # ==============================
    if pose_counter >= required_frames and stable_action != last_action:
        song_map = {
            "verse": "verse.mp3",
            "verse2": "verse 2.mp3",
            "chorus": "chorus.mp3",
            "bridge": "bridge.mp3"
        }

        if stable_action in song_map:
            song = song_map[stable_action]
            if os.path.exists(song):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                print(f">> POSE AKTIF: {stable_action.upper()}")

        last_action = stable_action

    # ==============================
    # 7. GRAFIK REAL-TIME
    # ==============================
    chart = np.zeros((chart_height, chart_width, 3), dtype=np.uint8)

    for i, label in enumerate(labels):
        val = scores[label.lower()]
        w = int(val * bar_width)
        color = (0, 255, 0) if val > 0 else (80, 80, 80)

        y_pos = i * 70 + 30

        cv2.rectangle(chart, (110, y_pos),
                      (110 + w, y_pos + bar_height),
                      color, -1)

        cv2.putText(chart, label, (10, y_pos + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255), 1)

        cv2.putText(chart, f"{int(val*100)}%",
                    (120 + w, y_pos + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (200, 200, 200), 1)

    # ==============================
    # 8. TAMPILAN
    # ==============================
    cv2.rectangle(frame, (0, 0), (300, 60), (0, 0, 0), -1)
    cv2.putText(frame, f"POSE: {stable_action.upper()}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Smart Pose Controller", frame)
    cv2.imshow("Real-time Pose Accuracy", chart)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==============================
# 9. CLEANUP
# ==============================
camera.release()
cv2.destroyAllWindows()
pygame.mixer.quit()