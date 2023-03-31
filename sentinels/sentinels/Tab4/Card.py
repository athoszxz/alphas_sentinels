from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit,\
    QPushButton, QMessageBox
from PyQt6.QtGui import QImage, QPixmap
import os
import psycopg2
from PyQt6 import QtCore


class Card(QWidget):
    def __init__(self, user_postgresql, password_postgresql):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.initUI()

    def initUI(self):
        # Cria um layout vertical para o Card
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

        form_v_layout.addWidget(self.cpf_textbox)
        form_v_layout.addWidget(self.search_button)

        # Cria uma label para ser o contorno do card
        self.user_info_label = QLabel(self)
        # Define o tamanho da label
        self.user_info_label.setFixedSize(300, 500)
        # Adiciona bordas à label
        self.user_info_label.setStyleSheet(
            "border: 3px solid black; background-color: green;")
        # Adiciona a label ao layout
        form_v_layout.addWidget(
            self.user_info_label,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # Centraliza as labels dentro do card

        # Criar os campos do Card:
        # Foto
        self.profile_picture = QLabel(self)
        self.profile_picture.setFixedSize(170, 175)
        self.profile_picture.move(65, 10)
        self.profile_picture.setStyleSheet(
            "border: 2px solid black; background-color: white;")
        self.profile_picture.setParent(self.user_info_label)
        self.profile_picture.setScaledContents(True)
        self.profile_picture.show()

        # Nome Completo
        self.first_name_label = QLabel("Nome Completo:", self)
        self.first_name_label.setFixedSize(210, 20)
        self.first_name_label.move(80, 200)
        self.first_name_label.setStyleSheet(
            "border: 0px solid red;"
            "text-align: center;"
            "font-size: 15px;"
            "font-weight: bold;"
            "color: white;")
        self.first_name_label.setParent(self.user_info_label)
        self.first_name_label.show()

        # CPF
        self.cpf_label = QLabel("CPF: ", self)
        self.cpf_label.setFixedSize(200, 20)
        self.cpf_label.move(80, 230)
        self.cpf_label.setStyleSheet(
            "border: 0px solid red;"
            "text-align: center;"
            "font-size: 15px;"
            "font-weight: bold;"
            "color: white;")
        self.cpf_label.setParent(self.user_info_label)
        self.cpf_label.show()

        # Data de nascimento
        self.date_label = QLabel("Data de nascimento: ", self)
        self.date_label.move(80, 260)
        self.date_label.setStyleSheet(
            "border: 0px solid red;"
            "text-align: center;"
            "font-size: 15px;"
            "font-weight: bold;"
            "color: white;")
        self.date_label.setParent(self.user_info_label)
        self.date_label.show()

        # Qr Code
        self.qr_code = QLabel(self)
        self.qr_code.setFixedSize(150, 175)
        self.qr_code.move(80, 300)
        self.qr_code.setStyleSheet(
            "border: 2px solid black; background-color: white;")
        self.qr_code.setScaledContents(True)
        self.qr_code.setParent(self.user_info_label)
        self.qr_code.show()

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
        cursor.execute(
            "SELECT p.photo, e.id_employee, e.first_name, e.last_name, " +
            "e.cpf, e.birth_date, e.qr_code " +
            "FROM employees e JOIN photos p ON e.id_employee = p.id_employee "
            + "WHERE p.id_photo = (SELECT MIN(id_photo) FROM photos " +
            "WHERE id_employee = e.id_employee)" +
            " AND e.cpf = %s", (cpf,))

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
            self.first_name_label.setText(name)
            self.cpf_label.setText('{}.{}.{}-{}'.format(cpf[:3], cpf[3:6],
                                                        cpf[6:9],
                                                        cpf[9:]))
            self.date_label.setText(str(format(birth_date, "%d/%m/%Y")))
            self.qr_code.setPixmap(QPixmap(image_qr_code))

        connection.commit()
        connection.close()

        return True

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
