from PyQt6.QtWidgets import QWidget, QHBoxLayout
from Tab4.Card import Card


class Tab4Card(QWidget):
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
        self.card = Card(
            self.user_postgresql, self.password_postgresql)

        # Adiciona tudo ao layout principal
        main_h_layout.addWidget(self.card)

        # Define o layout principal
        self.setLayout(main_h_layout)

        # Exibe a janela
        self.show()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
