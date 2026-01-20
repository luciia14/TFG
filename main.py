# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_definitions import right_arm_90deg_correct

def main():
    pose_cam = PoseCamera("pose_landmarker.task")
    last_time = time.time()

    print("Presiona Ctrl+C para salir")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            current_time = time.time()

            # Cada 3 segons
            if result.pose_landmarks and current_time - last_time >= 3:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)

                # Mostrar angles
                print(
                    f"R Elbow: {angles['right_elbow']:.1f}° | "
                    f"L Elbow: {angles['left_elbow']:.1f}° | "
                    f"R Shoulder: {angles['right_shoulder']:.1f}° | "
                    f"L Shoulder: {angles['left_shoulder']:.1f}°"
                )

                # Comprovar postura
                if right_arm_90deg_correct(angles):
                    print(">>> POSICIÓ CORRECTA <<<")
                else:
                    print("posició incorrecta")

                print("-" * 50)
                last_time = current_time

            # Només vídeo (sense text)
            cv2.imshow("Pose estimation", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Saliendo...")

    finally:
        pose_cam.release()

if __name__ == "__main__":
    main()

