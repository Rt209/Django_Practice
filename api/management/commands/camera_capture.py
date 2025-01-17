import cv2
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Post  

class Command(BaseCommand):
    help = "Capture images from the camera and save them."

    def handle(self, *args, **kwargs):
        SAVE_PATH = "media/captured_images/"
        os.makedirs(SAVE_PATH, exist_ok=True)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.stdout.write("Fail to open the camera...")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                self.stdout.write("Error reading frame.")
                break

            cv2.imshow("Live Camera Feed", frame)

            if (cv2.waitKey(1) & 0xFF == ord('p') or cv2.waitKey(1) & 0xFF == ord('P')):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"capture_{timestamp}.jpg"
                file_path = os.path.join(SAVE_PATH, file_name)

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                cv2.imwrite(file_path, gray_frame)
                self.stdout.write(f"Captured and saved as grayscale: {file_path}")

                Post.objects.create(picture=f"captured_images/{file_name}")

            # 按下 'q' 鍵退出
            if (cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q')):
                break

        cap.release()
        cv2.destroyAllWindows()