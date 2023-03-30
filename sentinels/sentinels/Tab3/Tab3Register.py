from PyQt6.QtWidgets import QWidget, QHBoxLayout
from Tab3.RegisterForm import RegisterForm
from Tab3.RegisterCam import RegisterCam


class Tab3Register(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.total_images = 0
        self.photos = []
        self.initUI()

    def initUI(self):
        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Adiciona o formulário de registro
        self.register_form = RegisterForm(
            self.user_postgresql, self.password_postgresql)

        # Adiciona a câmera
        self.register_cam = RegisterCam(self.cap, self.register_form)

        # Adiciona tudo ao layout principal
        main_h_layout.addWidget(self.register_form)
        main_h_layout.addWidget(self.register_cam)

        # Define o layout principal
        self.setLayout(main_h_layout)

        # Exibe a janela
        self.show()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.register_cam.cap.release()
        self.register_cam.timer.stop()
        self.register_cam.video_label.clear()

    def closeEvent(self, event):
        # Parar a câmera quando a janela for fechada
        self.register_cam.cap.release()
        self.register_cam.timer.stop()
        event.accept()
