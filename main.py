# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_arm_angle

def main():
    pose_cam = PoseCamera("pose_landmarker.task")
    last_time = time.time()
    angle_text = ""

    print("Presiona Ctrl+C per a eixir")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            current_time = time.time()

            if result.pose_landmarks and current_time - last_time >= 3:
                landmarks = result.pose_landmarks[0]
                angle = get_arm_angle(landmarks, frame.shape, side="right")
                angle_text = f"Angle braç dret: {angle:.1f}°"
                print(angle_text)
                last_time = current_time

            # Mostrar angle en pantalla
            cv2.putText(frame, angle_text, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Pose estimation", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC per tancar
                break

    except KeyboardInterrupt:
        print("Eixint...")

    finally:
        pose_cam.release()

if __name__ == "__main__":
    main()
