from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QDateEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QImage, QPixmap
import cv2
from PyQt6 import QtCore
import uuid
import os
import psycopg2
import io
import qrcode


class Card(QWidget):
    def __init__(self, user_postgresql, password_postgresql):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.initUI()

    def initUI(self):
        # Cria um layout vertical para o formulário
        form_v_layout = QVBoxLayout()

        # Caixa para pesquisar por CPF
        self.cpf_textbox = QLineEdit(self)
        self.cpf_textbox.move(90, 60)
        self.cpf_textbox.setFixedWidth(200)

        # Botão
        self.search_button = QPushButton("Pesquisar", self)
        self.search_button.move(100, 180)
        self.search_button.clicked.connect(self.search_data)
        # Diminui o tamanho do botão
        self.search_button.setFixedWidth(100)
        self.search_button.setFixedHeight(50)

        # Criar os campos do Card:
        # Foto
        self.profile_picture = QLabel(self)
        self.profile_picture.setFixedSize(125, 150)
        self.profile_picture.setStyleSheet("border: 1px solid black;")
        self.profile_picture.setScaledContents(True)

        # Nome Completo
        self.first_name_label = QLabel("Nome Completo:", self)
        self.first_name_label.move(20, 20)

        # CPF
        self.cpf_label = QLabel("CPF: ", self)
        self.cpf_label.move(20, 100)

        # Data de nascimento
        self.date_label = QLabel("Data de nascimento: ", self)
        self.date_label.move(20, 100)

        # Qr Code
        self.qr_code = QLabel(self)
        self.qr_code.setFixedSize(125, 150)
        self.qr_code.setStyleSheet("border: 1px solid black;")
        self.qr_code.setScaledContents(True)

        # Adiciona tudo ao layout do Card
        form_v_layout.addWidget(self.cpf_textbox)
        form_v_layout.addWidget(self.search_button)

        form_v_layout.addWidget(self.profile_picture)
        form_v_layout.addWidget(self.first_name_label)
        form_v_layout.addWidget(self.cpf_label)
        form_v_layout.addWidget(self.date_label)
        form_v_layout.addWidget(self.qr_code)

        # Adiciona o layout do formulário ao layout da janela
        self.setLayout(form_v_layout)

    def search_data(self):
        cpf = self.cpf_textbox.text()
        # Conectar ao banco de dados
        try:
            connection = psycopg2.connect(host="localhost",
                                          database="db_alphas_" +
                                          "sentinels_2023_144325",
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
        except (Exception, psycopg2.Error, psycopg2.OperationalError):
            # Verificar se o arquivo data.txt existe e excluí-lo
            if os.path.exists("data.txt"):
                os.remove("data.txt")
            self.show_message_box("Erro ao conectar ao banco de dados!" +
                                  "\nUsuário e/ou senha incorretos." +
                                  "\nVerifique se o PostgreSQL está rodando.")
            return False
        cursor = connection.cursor()

        # Pesquisar os dados no banco de dados
        cursor.execute('SELECT p.photo, e.id_employee, e.first_name, ' +
                       ' e.last_name, e.cpf, e.birth_date,e.qr_code ' +
                       ' FROM employees as e, photos as p ' +
                       ' WHERE e.id_employee = p.id_employee ' +
                       ' And p.profile_photo = %s ' +
                       ' AND e.cpf = %s ', ('true', str(cpf)))

        rows = cursor.fetchall()
        # self.table.setRowCount(len(rows))

        if len(rows) < 1:
            self.profile_picture.clear()
            self.first_name_label.setText("Nome Completo: ")
            self.cpf_label.setText("CPF: ")
            self.date_label.setText("Data de Nascimento: ")
            self.qr_code.clear()
            self.show_message_box("CPF não encontrado!")

        else:
            data = rows[0]
            profile = data[0]
            name = data[2] + " " + data[3]
            cpf = data[4]
            birth_date = data[5]
            qrcode = data[6]

            # Criar um objeto de imagem
            image = QImage()
            image_qr_code = QImage()

            # Carregar a imagem
            image.loadFromData(profile)
            image_qr_code.loadFromData(qrcode)

            self.profile_picture.setPixmap(QPixmap(image))
            self.first_name_label.setText("Nome Completo: \n" + name)
            self.cpf_label.setText(
                "CPF: \n" + '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
            self.date_label.setText(
                "Data de Nascimento: \n" + str(format(birth_date, "%d/%m/%Y")))
            self.qr_code.setPixmap(QPixmap(image_qr_code))

        connection.commit()
        connection.close()

        return True

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
