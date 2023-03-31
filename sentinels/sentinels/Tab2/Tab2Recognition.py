import cv2
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from Tab2.QrFaceRecognition import QrFaceRecognition
import pickle
import dlib
import sys
import os


class Tab2Recognition(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def initUI(self):
        # Carregar apenas uma vez o modelo criado com o pickle se ele existir
        try:
            with open('training/face_model5.pkl', 'rb') as f:
                self.descriptors = pickle.load(f)
        except FileNotFoundError:
            self.descriptors = []

        # Pegar o path do shape_predictor_68_face_landmarks.dat para
        # Pyinstaller e Python normal
        if getattr(sys, 'frozen', False):
            # executando como um executável gerado pelo PyInstaller
            path_shape = os.path.join(sys._MEIPASS, 'Tab2',
                                      'shape_predictor_68_face_landmarks.dat')
        else:
            # executando como um arquivo Python normal
            path_shape = 'Tab2/shape_predictor_68_face_landmarks.dat'

        # Pegar o path do dlib_face_recognition_resnet_model_v1.dat para
        # Pyinstaller e Python normal
        if getattr(sys, 'frozen', False):
            # executando como um executável gerado pelo PyInstaller
            path_recognition = os.path.join(
                sys._MEIPASS, 'Tab2',
                'dlib_face_recognition_resnet_model_v1.dat')
        else:
            # executando como um arquivo Python normal
            path_recognition = 'Tab2/dlib_face_recognition_resnet_model_v1.dat'

        # Pegar o path do haarcascade_frontalface_default.xml para
        # Pyinstaller e Python normal
        if getattr(sys, 'frozen', False):
            # executando como um executável gerado pelo PyInstaller
            path_cascade = os.path.join(sys._MEIPASS, 'Tab2',
                                        'haarcascade_frontalface_default.xml')
        else:
            # executando como um arquivo Python normal
            path_cascade = 'Tab2/haarcascade_frontalface_default.xml'

        # Carregar
        self.sp = dlib.shape_predictor(path_shape)
        self.facerec = dlib.face_recognition_model_v1(path_recognition)

        # Usar um detector de face mais rápido
        self.face_cascade = cv2.CascadeClassifier(path_cascade)

        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Adiciona o QrFaceRecognition
        self.qr_face_recognition = QrFaceRecognition(
            self.descriptors, self.sp, self.facerec,
            self.face_cascade, self.user_postgresql, self.password_postgresql)

        # Adiciona tudo ao layout principal
        main_h_layout.addWidget(self.qr_face_recognition)

        # Define o layout principal
        self.setLayout(main_h_layout)

        # Exibe a janela
        self.show()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.qr_face_recognition.check_model()
        self.qr_face_recognition.camera.release()
        self.qr_face_recognition.timer.stop()
        self.qr_face_recognition.cam_power_button.setText('Iniciar')
        self.qr_face_recognition.cam_power = False
        self.qr_face_recognition.video_label.clear()
        return
