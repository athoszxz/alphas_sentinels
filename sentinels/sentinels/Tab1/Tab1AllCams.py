from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
import os
import sys


class Tab1AllCams(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def initUI(self):
        # obter o caminho absoluto da pasta "icons" dentro do executável
        if getattr(sys, 'frozen', False):
            # o código está sendo executado a partir do executável
            icons_dir = os.path.join(sys._MEIPASS, 'icons')
        else:
            # o código está sendo executado a partir do arquivo Python original
            icons_dir = os.path.join(os.getcwd(), 'icons')

        # obter o caminho absoluto da logo1.png dentro do executável
        logo_path = os.path.join(icons_dir, "logo.jpg")

        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Cria uma label para exibir a logo da empresa
        self.logo_label = QLabel(self)
        self.logo_label.move(20, 20)
        self.logo_label.resize(300, 300)
        self.logo_label.setFixedSize(250, 200)
        self.logo_label.setScaledContents(True)
        self.logo_label.setPixmap(QPixmap(logo_path))

        # Cria outra label para exibir outra logo
        self.logo_label2 = QLabel(self)
        self.logo_label2.move(20, 20)
        self.logo_label2.resize(300, 300)
        self.logo_label2.setFixedSize(250, 200)
        self.logo_label2.setScaledContents(True)
        self.logo_label2.setPixmap(QPixmap(logo_path))
        # Redimensiona a imagem para 300x300

        # Adiciona a label ao layout horizontal principal
        main_h_layout.addWidget(self.logo_label)
        main_h_layout.addWidget(self.logo_label2)

        # Define o layout principal
        self.setLayout(main_h_layout)

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
