import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import face_recognition
import os

class FaceRecognitionApp:
    def __init__(self, root):
        # Tkinter 루트 윈도우 설정
        self.root = root
        self.root.title("Face Recognition App")

        # 이미지 표시를 위한 레이블 생성
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=20)

        # 이미지 업로드 버튼 생성
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 이미지 삭제 버튼 생성
        self.delete_button = tk.Button(root, text="Delete Image", command=self.delete_image)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # 이미지 경로를 저장할 변수 초기화
        self.image_path = None

    def upload_image(self):
        # 파일 선택 대화상자를 열어 이미지 파일을 선택하도록 설정
        self.image_path = filedialog.askopenfilename(
            title="Select an Image",
            initialdir=os.path.expanduser("~/"),  # 초기 디렉토리를 사용자 홈 디렉토리로 설정
            filetypes=[
                ("JPEG files", "*.jpg"),    # JPG 파일을 위한 항목 추가
                ("JPEG files", "*.jpeg"),   # JPEG 파일을 위한 항목 추가
                ("PNG files", "*.png"),     # PNG 파일을 위한 항목 추가
                ("BMP files", "*.bmp"),     # BMP 파일을 위한 항목 추가
                ("GIF files", "*.gif"),     # GIF 파일을 위한 항목 추가
                ("TIFF files", "*.tiff"),   # TIFF 파일을 위한 항목 추가
                ("WEBP files", "*.webp"),   # WEBP 파일을 위한 항목 추가
                ("All Files", "*.*")        # 모든 파일을 선택 가능하게 설정
            ]
        )
        if self.image_path:
            # 이미지를 화면에 표시하고 얼굴 인식을 수행
            self.display_image(self.image_path)
            self.recognize_faces(self.image_path)

    def delete_image(self):
        # 이미지 레이블을 초기화하여 이미지를 삭제
        if self.image_label.image:
            self.image_label.config(image='')
            self.image_path = None
            messagebox.showinfo("Info", "Image deleted")

    def display_image(self, image_path):
        # Pillow를 사용해 이미지를 열고 크기를 조정한 후 Tkinter에서 사용할 수 있는 형식으로 변환
        image = Image.open(image_path)
        image = image.resize((400, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        # 레이블에 이미지를 설정하여 화면에 표시
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def recognize_faces(self, image_path):
        # face_recognition 라이브러리로 이미지를 로드하고 얼굴 위치를 감지
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)

        # 얼굴이 감지되면 감지된 얼굴 수를 알림, 그렇지 않으면 알림 표시
        if face_locations:
            messagebox.showinfo("Result", f"Found {len(face_locations)} face(s)")
        else:
            messagebox.showinfo("Result", "No faces found")

if __name__ == "__main__":
    # Tkinter 루트 윈도우 생성 및 애플리케이션 실행
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
