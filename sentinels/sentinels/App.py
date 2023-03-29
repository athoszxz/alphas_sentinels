from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Tab1.Tab1AllCams import Tab1AllCams
from Tab2.Tab2Register import Tab2Register
from Tab3.Tab3Register import Tab3Register
from Tab4.Tab4Search import Tab4Search
import cv2


class App(QWidget):
    def __init__(self, user="", password=""):
        super().__init__()
        self.title = "Alpha's Sentinels"
        self.left = 500
        self.top = 200
        self.width = 960
        self.height = 760
        self.user_postgresql = user
        self.password_postgresql = password
        self.cap = cv2.VideoCapture(0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.cap.release()
        # cria o widget de abas
        tabs = QTabWidget()

        # cria as abas
        tab1 = Tab1AllCams(
            self.user_postgresql, self.password_postgresql, self.cap)
        tab2 = Tab2Register(
            self.user_postgresql, self.password_postgresql, self.cap)
        tab3 = Tab3Register(
            self.user_postgresql, self.password_postgresql, self.cap)
        tab4 = Tab4Search(
            self.user_postgresql, self.password_postgresql, self.cap)

        # adiciona as abas ao widget de abas
        tabs.addTab(tab1, "Todas as câmeras")
        tabs.addTab(tab2, "Reconhecimento")
        tabs.addTab(tab3, "Cadastro")
        tabs.addTab(tab4, "Busca")

        # Ao trocar de aba, fecha a webcam da aba anterior e abre a webcam da
        # aba atual
        tabs.currentChanged.connect(tab1.close_camera)
        tabs.currentChanged.connect(tab2.close_camera)
        tabs.currentChanged.connect(tab3.close_camera)
        tabs.currentChanged.connect(tab4.close_camera)

        # adiciona o widget de abas à janela
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

        self.show()

    def closeEvent(self, event):
        self.cap.release()
        event.accept()
