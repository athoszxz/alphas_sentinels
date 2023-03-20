from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Tab1AllCams import Tab1AllCams
from Tab2Register import Tab2Register
# from CreatePostgres import CreatePostgres


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
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # # Cria o banco de dados se não existir
        # create_db = CreatePostgres(self.user_postgresql,
        #                            self.password_postgresql)
        # create_db.check()

        # cria o widget de abas
        tabs = QTabWidget()

        # cria as abas
        tab1 = Tab1AllCams(self.user_postgresql, self.password_postgresql)
        tab2 = Tab2Register(self.user_postgresql, self.password_postgresql)

        # adiciona as abas ao widget de abas
        tabs.addTab(tab1, "Todas as câmeras")
        tabs.addTab(tab2, "Cadastrar Usuário")

        # adiciona o widget de abas à janela
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)

        self.show()
