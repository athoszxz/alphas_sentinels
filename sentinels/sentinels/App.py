from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Tab2.Tab2Recognition import Tab2Recognition
from Tab3.Tab3Register import Tab3Register
from Tab4.Tab4Card import Tab4Card
import cv2


class App(QWidget):
    def __init__(self, port: str = "", user: str = "", password: str = ""):
        super().__init__()
        self.title: str = "Alpha's Sentinels"
        self.port_postgresql: str = port
        self.user_postgresql: str = user
        self.password_postgresql: str = password
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(500, 200, 960, 760)
        self.cap.release()
        # cria o widget de abas
        tabs = QTabWidget()

        # cria as abas
        # tab1 = Tab1AllCams(
        #     self.user_postgresql, self.password_postgresql, self.cap)
        tab2 = Tab2Recognition(self.port_postgresql,
                               self.user_postgresql, self.password_postgresql,
                               self.cap)
        tab3 = Tab3Register(self.port_postgresql,
                            self.user_postgresql, self.password_postgresql,
                            self.cap)
        tab4 = Tab4Card(self.port_postgresql,
                        self.user_postgresql, self.password_postgresql,
                        self.cap)

        # adiciona as abas ao widget de abas
        # tabs.addTab(tab1, "Todas as câmeras")
        tabs.addTab(tab2, "Reconhecimento")
        tabs.addTab(tab3, "Cadastro")
        tabs.addTab(tab4, "Busca")

        # Ao trocar de aba, fecha a webcam da aba anterior e abre a webcam da
        # aba atual
        # tabs.currentChanged.connect(tab1.close_camera)
        tabs.currentChanged.connect(tab2.close_camera)
        tabs.currentChanged.connect(tab3.close_camera)
        tabs.currentChanged.connect(tab4.close_camera)

        # adiciona o widget de abas à janela
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

        self.show()

    def closeEvent(self, event) -> None:
        self.cap.release()
        event.accept()
