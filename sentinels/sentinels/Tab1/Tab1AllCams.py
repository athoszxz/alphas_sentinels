import psycopg2
import os
import io
import qrcode
import uuid
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,\
    QFileDialog, QMessageBox, QDateEdit


class Tab1AllCams(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        # self.title = "Todas as câmeras"
        # self.left = 500
        # self.top = 200
        # self.width = 960
        # self.height = 760
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def generate_qrcode(self, uuid):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uuid)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        # converter a imagem em binário
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr)
        return img_byte_arr.getvalue()

    def initUI(self):
        # Criar os campos do formulário

        # Nome
        self.first_name_label = QLabel("Nome", self)
        self.first_name_label.move(20, 20)
        self.first_name_textbox = QLineEdit(self)
        self.first_name_textbox.move(90, 20)

        # Sobrenome
        self.last_name_label = QLabel("Sobrenome", self)
        self.last_name_label.move(20, 60)
        self.last_name_textbox = QLineEdit(self)
        self.last_name_textbox.move(90, 60)

        # Data de nascimento
        self.date_label = QLabel("Data de nascimento", self)
        self.date_label.move(20, 100)
        self.date_input_textbox = QDateEdit(self)
        self.date_input_textbox.move(140, 100)

        # Cria o botão de Adicionar imagem
        self.open_image_button = QPushButton("Adicionar imagem", self)
        self.open_image_button.move(20, 140)
        self.open_image_button.clicked.connect(self.open_image)

        # Cria o botão de enviar
        self.submit_button = QPushButton("Enviar", self)
        self.submit_button.move(100, 180)
        self.submit_button.clicked.connect(self.submit_data)

    def open_image(self):
        # Abrir a janela de seleção de arquivo
        file_name = QFileDialog.getOpenFileName(self, "Abrir imagem", "",
                                                "Imagens (*.png *.jpg)")[0]
        if file_name:
            # Ler o arquivo binário
            with open(file_name, "rb") as f:
                self.image = f.read()

    def submit_data(self):
        # Gerar um ID único para o usuário
        user_id = uuid.uuid4()
        # Pegar os valores dos campos
        first_name = self.first_name_textbox.text()
        last_name = self.last_name_textbox.text()
        date = self.date_input_textbox.text()
        qrcode = self.generate_qrcode(user_id)

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

        # Inserir os dados no banco de dados
        cursor.execute('INSERT INTO employees ' +
                       '(id_employee, first_name, '
                       + 'last_name, birth_date, qr_code) '
                       'VALUES (%s, %s, %s, %s, %s)',
                       (str(user_id), str(first_name), last_name, date,
                        psycopg2.Binary(qrcode)))

        connection.commit()
        connection.close()
        self.show_message_box("Dados enviados com sucesso!")

        # Limpar os campos
        self.first_name_textbox.setText("")
        self.last_name_textbox.setText("")
        self.date_input_textbox.setText("")

        return True

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
