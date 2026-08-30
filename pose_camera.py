import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Conexiones del esqueleto
POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28),
    (27, 29), (28, 30),
    (29, 31), (30, 32),
]


class PoseCamera:
    def __init__(self, model_path, camera_source=None):
        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

        
        if camera_source is None:
            self.camera_url = "http://192.168.1.100/stream"
        else:
            self.camera_url = camera_source

        self.cap = cv2.VideoCapture(self.camera_url)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"No se puede conectar al streaming de la ESP en: {self.camera_url}")

    def _draw_landmarks(self, image, detection_result):
        annotated_image = image.copy()

        if detection_result.pose_landmarks:
            for landmark_list in detection_result.pose_landmarks:

                # Dibujar esqueleto
                for start_idx, end_idx in POSE_CONNECTIONS:
                    p1 = landmark_list[start_idx]
                    p2 = landmark_list[end_idx]

                    x1 = int(p1.x * image.shape[1])
                    y1 = int(p1.y * image.shape[0])
                    x2 = int(p2.x * image.shape[1])
                    y2 = int(p2.y * image.shape[0])

                    cv2.line(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Dibujar puntos
                for point in landmark_list:
                    x = int(point.x * image.shape[1])
                    y = int(point.y * image.shape[0])
                    cv2.circle(annotated_image, (x, y), 4, (0, 0, 255), -1)

        return annotated_image

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            # Si se pierde la conexión momentáneamente con la ESP, puedes reintentar abrir
            return None, None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, frame_rgb)

        result = self.detector.detect(mp_image)
        annotated_rgb = self.id_draw_landmarks(frame_rgb, result) if hasattr(self, '_draw_landmarks') else self._draw_landmarks(frame_rgb, result)
        annotated_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)

        return annotated_bgr, result

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()