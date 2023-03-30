import cv2
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from Tab2.QrFaceRecognition import QrFaceRecognition
import pickle
import dlib


class Tab2Recognition(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def initUI(self):

        # Carregar apenas uma vez o modelo criado com o pickle
        with open('Tab2/face_model5.pkl', 'rb') as f:
            self.descriptors = pickle.load(f)

            # Criar apenas uma vez o detector de pontos faciais
        self.sp = dlib.shape_predictor(
            'Tab2/shape_predictor_68_face_landmarks.dat')
        self.facerec = dlib.face_recognition_model_v1(
            'Tab2/dlib_face_recognition_resnet_model_v1.dat')

        # Usar um detector de face mais rápido
        self.face_cascade = cv2.CascadeClassifier(
            'Tab2/haarcascade_frontalface_default.xml')

        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Adiciona o QrFaceRecognition
        self.qr_face_recognition = QrFaceRecognition(
            self.descriptors, self.sp, self.facerec,
            self.face_cascade, self.user_postgresql, self.password_postgresql)

        # Cria um widget teste com um botão
        self.teste = QWidget()
        self.teste.setLayout(QVBoxLayout())
        self.teste.layout().addWidget(QPushButton('Teste'))

        # Adiciona tudo ao layout principal
        main_h_layout.addWidget(self.qr_face_recognition)

        # Define o layout principal
        self.setLayout(main_h_layout)

        # Exibe a janela
        self.show()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.qr_face_recognition.camera.release()
        self.qr_face_recognition.timer.stop()
        self.qr_face_recognition.cam_power_button.setText('Iniciar')
        self.qr_face_recognition.cam_power = False
        self.qr_face_recognition.video_label.clear()
        return
