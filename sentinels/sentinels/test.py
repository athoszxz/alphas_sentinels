import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTabWidget,\
    QLabel, QVBoxLayout


class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        button1 = QPushButton("Hello World!", self)
        button1.clicked.connect(self.on_click)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(button1)
        self.setLayout(self.layout)

    # slot para o clique do botão
    def on_click(self):
        print("Hello World!")


class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label2 = QLabel("Aba 2 aqui!", self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(label2)
        self.setLayout(self.layout)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'My App'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # cria o widget de abas
        tabs = QTabWidget()

        # cria as abas
        tab1 = Tab1()
        tab2 = Tab2()

        # adiciona as abas ao widget de abas
        tabs.addTab(tab1, "Aba 1")
        tabs.addTab(tab2, "Aba 2")

        # adiciona o widget de abas à janela
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(tabs)
        self.setLayout(self.layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
