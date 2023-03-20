# You can run directly this code with: poetry run python test_postgresql.py
# But you need to have a PostgreSQL installed and running.
# You can download it from: https://www.postgresql.org/download/
# And you can install it with: pip install psycopg2 or poetry add psycopg2
# You don't need to create the database, the code will do it for you.
import sys
import os
from cryptography.fernet import Fernet
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit,\
    QLabel
from PyQt6.QtCore import pyqtSlot
from App import App
from CreatePostgres import CreatePostgres


class PostgreeForms(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PostgreSQL Login'
        self.left = 500
        self.top = 300
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label_user = QLabel("Usuário", self)
        self.label_user.move(20, 20)
        self.label_password = QLabel("Senha", self)
        self.label_password.move(20, 60)

        self.textbox_user = QLineEdit(self)
        self.textbox_user.move(80, 20)
        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.textbox_password.move(80, 60)

        self.button_submit = QPushButton('Enviar', self)
        self.button_submit.clicked.connect(self.on_click_submit)
        self.button_submit.resize(80, 30)
        self.button_submit.move(200, 120)

        self.check_file_exists()

    def check_file_exists(self):
        if os.path.exists("data.txt"):
            with open("data.txt", "rb") as f:
                token = f.readline()
                key = f.readline()
            f = Fernet(key)
            user, password = f.decrypt(token).decode().split(" ")
            result = self.create_database(user, password)
            if result:
                self.open_app(user, password)
                self.close()
        else:
            self.show()

    @pyqtSlot()
    def on_click_submit(self):
        user = self.textbox_user.text()
        password = self.textbox_password.text()
        result = self.create_database(user, password)
        if result:
            key = Fernet.generate_key()
            f = Fernet(key)
            token = f.encrypt(str.encode(user + " " + password))
            with open("data.txt", "wb") as f:
                f.write(token + b'\n')
                f.write(key)
            self.open_app(user, password)
            self.close()

    def open_app(self, user="", password=""):
        self.app = App(user, password)
        self.app.show()

    def create_database(self, user, password):
        create_postgres = CreatePostgres(user, password)
        return create_postgres.check()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PostgreeForms()
    sys.exit(app.exec())
