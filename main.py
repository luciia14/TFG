# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles

def main():
    pose_cam = PoseCamera("pose_landmarker.task")
    last_time = time.time()
    angles_text = ""

    print("Presiona Ctrl+C para salir")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            current_time = time.time()

            if result.pose_landmarks and current_time - last_time >= 3:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)

                # Formatear texto
                angles_text = (
                    f"R Elbow: {angles['right_elbow']:.1f}°  "
                    f"L Elbow: {angles['left_elbow']:.1f}°  "
                    f"R Shoulder: {angles['right_shoulder']:.1f}°  "
                    f"L Shoulder: {angles['left_shoulder']:.1f}°"
                )
                print(angles_text)
                last_time = current_time

            
            cv2.imshow("Pose estimation", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC para cerrar
                break

    except KeyboardInterrupt:
        print("Saliendo...")

    finally:
        pose_cam.release()

if __name__ == "__main__":
    main()
