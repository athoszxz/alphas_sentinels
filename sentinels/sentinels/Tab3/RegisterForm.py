from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QDateEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import cv2
from PyQt6 import QtCore
import uuid
import os
import psycopg2
import io
import qrcode


class RegisterForm(QWidget):
    def __init__(self, user_postgresql, password_postgresql):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.image_1 = QLabel(self)
        self.image_2 = QLabel(self)
        self.image_3 = QLabel(self)
        self.image_4 = QLabel(self)
        self.image_5 = QLabel(self)
        self.image_6 = QLabel(self)
        self.total_images = 0
        self.photos = []
        self.initUI()

    def initUI(self):
        # Cria um layout vertical para o formulário
        form_v_layout = QVBoxLayout()

        # Criar os campos do formulário:

        # Nome
        self.first_name_label = QLabel("Nome", self)
        self.first_name_textbox = QLineEdit(self)
        # Diminui o tamanho da caixa de texto e da label
        self.first_name_label.setFixedWidth(200)
        self.first_name_textbox.setFixedWidth(200)

        # Sobrenome
        self.last_name_label = QLabel("Sobrenome", self)

        self.last_name_textbox = QLineEdit(self)

        # Diminui o tamanho da caixa de texto e da label
        self.last_name_label.setFixedWidth(200)
        self.last_name_textbox.setFixedWidth(200)

        # CPF
        self.cpf_label = QLabel("CPF", self)

        self.cpf_textbox = QLineEdit(self)

        # Diminui o tamanho da caixa de texto e da label
        self.cpf_label.setFixedWidth(200)
        self.cpf_textbox.setFixedWidth(200)

        # Data de nascimento
        self.date_label = QLabel("Data de nascimento", self)

        self.date_input_textbox = QDateEdit(self)

        # Diminui o tamanho da caixa de texto e da label
        self.date_label.setFixedWidth(200)
        self.date_input_textbox.setFixedWidth(200)

        # Cria um horizontalbox para adicionar 3 locais para exibir as imagens
        self.image_hbox = QHBoxLayout()
        self.image_hbox.setSpacing(10)
        self.image_hbox.setContentsMargins(0, 0, 0, 0)

        # Cria o local 1 para exibir a imagem com o tamanho de 125x150
        self.image_1.setFixedSize(125, 150)
        self.image_1.setStyleSheet("border: 1px solid black;")
        self.image_hbox.addWidget(self.image_1)

        # Cria o local 2 para exibir a imagem com o tamanho de 125x150
        self.image_2.setFixedSize(125, 150)
        self.image_2.setStyleSheet("border: 1px solid black;")
        self.image_hbox.addWidget(self.image_2)

        # Cria o local 3 para exibir a imagem com o tamanho de 125x150
        self.image_3.setFixedSize(125, 150)
        self.image_3.setStyleSheet("border: 1px solid black;")
        self.image_hbox.addWidget(self.image_3)

        # Cria um horizontalbox para adicionar 3 locais para exibir as imagens
        self.image_hbox2 = QHBoxLayout()
        self.image_hbox2.setSpacing(10)
        self.image_hbox2.setContentsMargins(0, 0, 0, 0)

        # Cria o local 4 para exibir a imagem com o tamanho de 125x150
        self.image_4.setFixedSize(125, 150)
        self.image_4.setStyleSheet("border: 1px solid black;")
        self.image_hbox2.addWidget(self.image_4)

        # Cria o local 5 para exibir a imagem com o tamanho de 125x150
        self.image_5.setFixedSize(125, 150)
        self.image_5.setStyleSheet("border: 1px solid black;")
        self.image_hbox2.addWidget(self.image_5)

        # Cria o local 6 para exibir a imagem com o tamanho de 125x150
        self.image_6.setFixedSize(125, 150)
        self.image_6.setStyleSheet("border: 1px solid black;")
        self.image_hbox2.addWidget(self.image_6)

        # Cria o botão de enviar
        self.submit_button = QPushButton("Enviar", self)
        self.submit_button.move(100, 180)
        self.submit_button.clicked.connect(self.submit_data)
        # Diminui o tamanho do botão
        self.submit_button.setFixedWidth(200)
        self.submit_button.setFixedHeight(50)
        # Muda as propriedades do botão
        self.submit_button.setStyleSheet("background-color:  #00bfff;"
                                         "color: white;"
                                         "font-weight: bold;"
                                         "font-size: 20px;"
                                         "border-radius: 10px;"
                                         "border: 2px solid black;")

        # Adiciona tudo ao layout do formulário
        form_v_layout.addWidget(self.first_name_label)
        form_v_layout.addWidget(self.first_name_textbox)
        form_v_layout.addWidget(self.last_name_label)
        form_v_layout.addWidget(self.last_name_textbox)
        form_v_layout.addWidget(self.cpf_label)
        form_v_layout.addWidget(self.cpf_textbox)
        form_v_layout.addWidget(self.date_label)
        form_v_layout.addWidget(self.date_input_textbox)
        form_v_layout.addLayout(self.image_hbox)
        form_v_layout.addLayout(self.image_hbox2)
        form_v_layout.addWidget(
            self.submit_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Adiciona o layout do formulário ao layout da janela
        self.setLayout(form_v_layout)

    def submit_data(self):
        # Gerar um ID único para o usuário
        user_id = uuid.uuid4()
        # Pegar os valores dos campos
        first_name = self.first_name_textbox.text()
        last_name = self.last_name_textbox.text()
        cpf = self.cpf_textbox.text()
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
                       + 'last_name, cpf, birth_date, qr_code) '
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (str(user_id), str(first_name), last_name, int(cpf),
                        date, psycopg2.Binary(qrcode)))

        # Inserir as fotos no banco de dados
        for i in range(self.total_images):
            # Converter a imagem para bytes já que estava em formato QImage
            _, buffer = cv2.imencode('.jpg', self.photos[i])

        cursor.execute('INSERT INTO photos (id_photo, id_employee, photo) '
                       + 'VALUES (%s, %s, %s)',
                       (str(uuid.uuid4()), str(user_id),
                         psycopg2.Binary(buffer.tobytes())))

        connection.commit()
        connection.close()
        self.show_message_box("Dados enviados com sucesso!")

        # Limpar os campos
        self.first_name_textbox.setText("")
        self.last_name_textbox.setText("")
        self.cpf_textbox.setText("")
        self.date_input_textbox.clear()
        self.clear_images()
        self.total_images = 0

        return True

    def generate_qrcode(self, uuid):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uuid)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        # converter a imagem em binário
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr)
        return img_byte_arr.getvalue()

    def add_image(self, frame, photos):
        self.total_images = len(photos)
        self.photos.append(frame)

        # Converter o frame para RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Converter o frame para QImage e pegar o centro da imagem
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line,
                                      QImage.Format.Format_RGB888)
        pixmap = convert_to_Qt_format.scaled(
            550, 650, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        # Espelhar a imagem
        pixmap = pixmap.mirrored(True, False)
        # Mover a imagem para o centro
        pixmap = pixmap.copy(250, 0, 300, 300)
        # Adicionar a imagem ao label
        if self.total_images == 1:
            self.image_1.setPixmap(QPixmap.fromImage(pixmap))
        elif self.total_images == 2:
            self.image_2.setPixmap(QPixmap.fromImage(pixmap))
        elif self.total_images == 3:
            self.image_3.setPixmap(QPixmap.fromImage(pixmap))
        elif self.total_images == 4:
            self.image_4.setPixmap(QPixmap.fromImage(pixmap))
        elif self.total_images == 5:
            self.image_5.setPixmap(QPixmap.fromImage(pixmap))
        elif self.total_images == 6:
            self.image_6.setPixmap(QPixmap.fromImage(pixmap))

    def clear_images(self):
        self.image_1.clear()
        self.image_2.clear()
        self.image_3.clear()
        self.image_4.clear()
        self.image_5.clear()
        self.image_6.clear()

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
