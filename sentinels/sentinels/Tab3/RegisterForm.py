from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QDateEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
import cv2
from PyQt6 import QtCore, QtGui
import uuid
import psycopg2
import io
import qrcode
from typing import List
from DataBase import DataBase


class RegisterForm(QWidget):
    def __init__(self, port_postgresql: str, user_postgresql: str,
                 password_postgresql: str) -> None:
        super().__init__()
        self.port_postgresql: str = port_postgresql
        self.user_postgresql: str = user_postgresql
        self.password_postgresql: str = password_postgresql
        self.image_1: QLabel = QLabel(self)
        self.image_2 = QLabel(self)
        self.image_3 = QLabel(self)
        self.image_4 = QLabel(self)
        self.image_5 = QLabel(self)
        self.image_6 = QLabel(self)
        self.total_images: int = 0
        self.photos: List[QLabel] = []
        self.initUI()

    def initUI(self):
        # Cria um layout vertical para o formulário
        form_v_layout = QVBoxLayout()

        # Criar os campos do formulário:

        # Nome
        self.first_name_label = QLabel("Nome", self)
        self.first_name_textbox = QLineEdit(self)
        # Só aceita letras, espaços, acentos e hífen
        self.first_name_textbox.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("[A-Za-zÀ-ú ]+")))

        # Diminui o tamanho da caixa de texto e da label
        self.first_name_label.setFixedWidth(200)
        self.first_name_textbox.setFixedWidth(200)

        # Sobrenome
        self.last_name_label = QLabel("Sobrenome", self)
        self.last_name_textbox = QLineEdit(self)
        # Só aceita letras, espaços, acentos e hífen
        self.last_name_textbox.setValidator(
            QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("[A-Za-zÀ-ú ]+")))

        # Diminui o tamanho da caixa de texto e da label
        self.last_name_label.setFixedWidth(200)
        self.last_name_textbox.setFixedWidth(200)

        # CPF
        self.cpf_label = QLabel("CPF", self)
        self.cpf_textbox = QLineEdit(self)
        # Só aceita números
        self.cpf_textbox.setValidator(QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(r'^\d{0,11}$')))

        # Diminui o tamanho da caixa de texto e da label
        self.cpf_label.setFixedWidth(200)
        self.cpf_textbox.setFixedWidth(200)

        # Data de nascimento
        self.date_label = QLabel("Data de nascimento", self)
        self.date_input_textbox = QDateEdit(self)
        self.date_input_textbox.setDisplayFormat("dd/MM/yyyy")
        self.date_input_textbox.setCalendarPopup(True)

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
        if self.first_name_textbox.text() == '' or \
            self.last_name_textbox.text() == '' or \
                self.cpf_textbox.text() == '' or \
                self.total_images < 6:
            # Show error message box
            msg = QMessageBox()
            msg.setText("Erro")
            msg.setInformativeText(
                "Por favor, preencha todos os campos obrigatórios.")
            msg.setWindowTitle("Erro")
            msg.exec()
            return

        # Gerar um ID único para o usuário
        user_id = (uuid.uuid4())
        # Pegar os valores dos campos
        first_name = self.first_name_textbox.text()
        last_name = self.last_name_textbox.text()
        cpf = self.cpf_textbox.text()
        date = self.date_input_textbox.text()
        qrcode = self.generate_qrcode(user_id)

        database = DataBase(self.port_postgresql,
                            "db_alphas_sentinels_2023_144325",
                            self.user_postgresql,
                            self.password_postgresql)
        database.connect(self)
        database.create(self, "employees",
                        "id_employee, first_name, last_name," +
                        " cpf, birth_date, qr_code",
                        [str(user_id), str(first_name), last_name, int(cpf),
                         date, psycopg2.Binary(qrcode)])

        # Inserir as fotos no banco de dados
        for i in range(self.total_images):
            # Converter a imagem para bytes já que estava em formato QImage
            _, buffer = cv2.imencode('.jpg', self.photos[i])

            database.create(self, "photos", "id_photo, id_employee, photo",
                            (str(uuid.uuid4()), str(user_id),
                             psycopg2.Binary(buffer.tobytes())))

        # Salvar as alterações
        database.commit()
        database.close()

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
