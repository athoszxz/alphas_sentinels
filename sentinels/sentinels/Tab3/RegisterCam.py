from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel,\
    QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import cv2
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer


class RegisterCam(QWidget):
    def __init__(self, cap, register_form):
        super().__init__()
        self.cap = cap
        self.register_form = register_form
        self.timer = QTimer(self)
        self.total_images = 0
        self.photos = []
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

        # Cria uma label para exibir a logo da empresa
        logo_label = QLabel(self)
        # Define o tamanho da label
        logo_label.setFixedSize(250, 200)
        # Redimensiona a imagem para caber na label
        logo_label.setScaledContents(True)
        # Adiciona a imagem à label
        logo_label.setPixmap(QPixmap('icons/logo.jpg'))

        # Adiciona os layouts à vertical da câmera
        camera_v_layout.addLayout(cam_power_button_h_layout)
        camera_v_layout.addWidget(self.video_label)
        camera_v_layout.addLayout(take_photo_button_h_layout)
        camera_v_layout.addWidget(logo_label)

        # Define o layout da janela
        self.setLayout(camera_v_layout)

        # Cria um Timer para atualizar a imagem da webcam
        self.timer.timeout.connect(self.update_frame)

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
