from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap


class Tab1AllCams(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def initUI(self):
        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Cria uma label para exibir a logo da empresa
        self.logo_label = QLabel(self)
        self.logo_label.move(20, 20)
        self.logo_label.resize(300, 300)
        self.logo_label.setFixedSize(250, 200)
        self.logo_label.setScaledContents(True)
        self.logo_label.setPixmap(QPixmap("icons/logo.jpg"))

        # Cria outra label para exibir outra logo
        self.logo_label2 = QLabel(self)
        self.logo_label2.move(20, 20)
        self.logo_label2.resize(300, 300)
        self.logo_label2.setFixedSize(250, 200)
        self.logo_label2.setScaledContents(True)
        self.logo_label2.setPixmap(QPixmap("icons/logo.jpg"))
        # Redimensiona a imagem para 300x300

        # Adiciona a label ao layout horizontal principal
        main_h_layout.addWidget(self.logo_label)
        main_h_layout.addWidget(self.logo_label2)

        # Define o layout principal
        self.setLayout(main_h_layout)

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
