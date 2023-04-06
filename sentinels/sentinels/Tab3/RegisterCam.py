from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel,\
    QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import cv2
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
import numpy as np
import os
import sys
import psycopg2
import dlib
import pickle
from typing import List


class RegisterCam(QWidget):
    def __init__(self, port_postgresql: str, cap: cv2.VideoCapture,
                 register_form: QWidget, user_postgresql: str,
                 password_postgresql: str) -> None:
        super().__init__()
        self.port_postgresql: str = port_postgresql
        self.user_postgresql: str = user_postgresql
        self.password_postgresql: str = password_postgresql
        self.cap: cv2.VideoCapture = cap
        self.register_form = register_form
        self.timer: QTimer = QTimer()
        self.total_images: int = 0
        self.photos: List = []
        self.initUI()

    def initUI(self):
        self.cap = cv2.VideoCapture(0)

        # Cria um layout vertical para a câmera
        camera_v_layout = QVBoxLayout()

        # Cria um layout horizontal para o botão de iniciar e parar a câmera
        cam_power_button_h_layout = QHBoxLayout()
        # Cria um botão para iniciar e parar a câmera
        self.cam_power_button = QPushButton('Iniciar', self)
        cam_power_button_h_layout.addWidget(self.cam_power_button)
        self.cam_power_button.clicked.connect(self.toggle_camera)
        # Redimensiona o botão
        self.cam_power_button.setFixedSize(100, 30)

        # Cria uma label para exibir a webcam
        self.video_label = QLabel(self)
        # Define o tamanho da label
        self.video_label.setFixedSize(250, 300)
        # Redimensiona a imagem para caber na label
        # self.video_label.setScaledContents(True)
        # Corta o lado esquerdo e direito da label em 10 pixels
        # self.video_label.setContentsMargins(100, 0, 100, 0)
        # Adiciona bordas à label
        self.video_label.setStyleSheet("border: 1px solid black;")

        # Cria um layout horizontal o botão de tirar foto
        take_photo_button_h_layout = QHBoxLayout()
        # Cria um botão para tirar foto
        self.take_photo_button = QPushButton('Tirar foto', self)
        take_photo_button_h_layout.addWidget(self.take_photo_button)
        self.take_photo_button.clicked.connect(self.take_photo)
        # Redimensiona o botão
        self.take_photo_button.setFixedSize(100, 30)

        # Cria um layout horizontal para o botão de treinar o modelo
        train_model_button_h_layout = QHBoxLayout()
        # Cria um botão para fazer o treinamento do modelo
        self.train_model_button = QPushButton('Treinar modelo', self)
        train_model_button_h_layout.addWidget(self.train_model_button)
        self.train_model_button.clicked.connect(self.train_model)
        # Redimensiona o botão
        self.train_model_button.setFixedSize(100, 30)

        # Adiciona os layouts à vertical da câmera
        camera_v_layout.addLayout(cam_power_button_h_layout)
        camera_v_layout.addWidget(self.video_label)
        camera_v_layout.addLayout(take_photo_button_h_layout)
        camera_v_layout.addLayout(train_model_button_h_layout)

        # Define o layout da janela
        self.setLayout(camera_v_layout)

        # Cria um Timer para atualizar a imagem da webcam
        self.timer.timeout.connect(self.update_frame)

    def train_model(self):
        # Criar uma conexão com o banco de dados
        try:
            conn = psycopg2.connect(host="localhost",
                                    port=self.port_postgresql,
                                    database="db_alphas_sentinels_2023_"
                                    + "144325",
                                    user=self.user_postgresql,
                                    password=self.password_postgresql)
        except psycopg2.OperationalError:
            QMessageBox.critical(self, 'Erro',
                                 'Não foi possível conectar ao banco de '
                                 'dados. Verifique se o PostgreSQL está '
                                 'rodando e se as credenciais estão '
                                 'corretas.')
            return

        # Criar um cursor
        cursor = conn.cursor()

        # Criar um detector de rosto usando o Detector de Pontos Faciais
        # de Dlib
        detector = dlib.get_frontal_face_detector()

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
            path_dlib = os.path.join(
                sys._MEIPASS, 'Tab2',
                'dlib_face_recognition_resnet_model_v1.dat')
        else:
            # executando como um arquivo Python normal
            path_dlib = 'Tab2/dlib_face_recognition_resnet_model_v1.dat'

        # Criar um modelo de Reconhecimento Facial usando o Modelo ResNet
        # do Dlib
        sp = dlib.shape_predictor(path_shape)
        facerec = dlib.face_recognition_model_v1(path_dlib)

        # Criar um array para armazenar os vetores de descritor facial
        descriptors = []

        # Criar um array para armazenar os rótulos
        labels = []

        # Buscar todas as fotos do banco de dados
        cursor.execute("SELECT id_photo, id_employee, photo FROM photos")
        photos = cursor.fetchall()

        # Para cada foto, detectar o rosto e calcular o descritor facial
        for photo in photos:
            id_employee = photo[1]
            photo_data = photo[2]
            nparr = np.frombuffer(photo_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            dets = detector(img, 1)
            for det in dets:
                shape = sp(img, det)
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                descriptors.append(face_descriptor)
                labels.append(id_employee)

        # Verificar se a pasta 'training' existe
        if not os.path.exists('training'):
            # Criar a pasta 'training'
            os.makedirs('training')

        # Salvar o modelo criado como um arquivo
        with open('training/face_model5.pkl', 'wb') as f:
            pickle.dump({'descriptors': descriptors, 'labels': labels}, f)

        # Fechar a conexão com o banco de dados
        conn.close()

        # Desabilitar botão de treinar modelo por 10 segundos
        self.train_model_button.setEnabled(False)
        QtCore.QTimer.singleShot(
            30000, lambda: self.train_model_button.setEnabled(True))

        return

    def toggle_camera(self):
        if self.cap.isOpened():
            self.cap.release()
            self.timer.stop()
            self.cam_power_button.setText('Iniciar')
            self.video_label.clear()
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(0)
            self.timer.start(30)
            self.cam_power_button.setText('Parar')

    def take_photo(self):
        # Verificar se a câmera está aberta
        if not self.cap.isOpened():
            return

        if self.total_images >= 6:
            QMessageBox.warning(self, "Erro", "Limite de fotos atingido")
            return

        # Ler o frame da webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Ler o frame da webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Array com as fotos
        self.photos.append(frame)

        # Adicionar a imagem ao formulário de registro
        self.register_form.add_image(frame,
                                     self.photos)

        # Incrementar o total de fotos
        self.total_images += 1

    def update_frame(self):
        # Verificar se a câmera está aberta
        if not self.cap.isOpened():
            return

        # Ler o frame da webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Converter o frame para RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Converter o frame para QImage e pegar o centro da imagem
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line,
                                      QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            550, 650, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # Espelhar a imagem
        p = p.mirrored(True, False)
        # Mover a imagem para o centro
        p = p.copy(200, 0, 300, 300)

        # Exibir a imagem na label
        self.video_label.setPixmap(QPixmap.fromImage(p))

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
        self.timer.stop()
        self.video_label.clear()

    def closeEvent(self, event):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
        self.timer.stop()
        event.accept()
