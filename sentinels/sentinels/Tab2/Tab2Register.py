import psycopg2
import cv2
import os
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog
from PyQt6.QtGui import QImage, QPixmap


class Tab2Register(QWidget):
    def __init__(self, user_postgresql, password_postgresql, cap):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.cap = cap
        self.initUI()

    def open_image(self):
        # Abrir a janela de seleção de arquivo
        file_name = QFileDialog.getOpenFileName(self, "Abrir imagem", "",
                                                "Imagens (*.png *.jpg)")[0]
        if file_name:
            # Ler o arquivo binário
            with open(file_name, "rb") as f:
                self.image = f.read()

    def initUI(self):
        # Cria um botão para ligar/desligar a webcam
        self.toggle_webcam_button = QPushButton("Ligar webcam", self)
        self.toggle_webcam_button.move(20, 90)
        self.toggle_webcam_button.clicked.connect(self.toggle_webcam)

        # Cria um local para exibir o video da webcam
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(580, 300)
        self.video_label.move(350, 20)
        self.video_label.setScaledContents(True)

        # Cria um botão para tirar uma foto
        self.take_photo_button = QPushButton("Tirar foto", self)
        self.take_photo_button.move(20, 120)
        self.take_photo_button.clicked.connect(self.take_photo)

        # Cria o botão de Adicionar imagem
        self.open_image_button = QPushButton("Adicionar imagem", self)
        self.open_image_button.move(20, 140)
        self.open_image_button.clicked.connect(self.open_image)

        # Criar a tabela
        self.table = QTableWidget(self)
        self.table.move(20, 250)
        self.table.resize(300, 200)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome", "Sobrenome", "Idade"])

        # Cria um local para exibir a imagem com o tamanho de 300x300
        self.image_label = QLabel(self)
        self.image_label.move(20, 470)
        self.image_label.resize(150, 150)
        # faz a imagem caber no label
        self.image_label.setScaledContents(True)

        # Cria uma caixa de texto para pegar o id
        self.id_textbox = QLineEdit(self)
        self.id_textbox.move(20, 650)
        self.id_textbox.resize(100, 30)

        # Cria o botão de buscar imagem
        self.search_image_button = QPushButton("Buscar imagem", self)
        self.search_image_button.move(20, 680)
        self.search_image_button.clicked.connect(self.search_image)

        # Executar a consulta SQL para recuperar os dados
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
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        # Preencher a tabela com os dados ignorando o ID
        for i, row in enumerate(rows):
            for j, field in enumerate(row[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(field)))

        self.show()
        return True

    def search_image(self):
        # Pegar o ID do usuário
        user_id = self.id_textbox.text()
        # Executar a consulta SQL para recuperar os dados
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
        cursor.execute(
            "SELECT qr_code FROM employees WHERE id_employee = %s", (user_id,))
        photo = cursor.fetchone()[0]
        # Criar um objeto de imagem
        image = QImage()
        # Carregar a imagem
        image.loadFromData(photo)
        # Exibir a imagem
        self.image_label.setPixmap(QPixmap(image))

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
        # exit()

    def toggle_webcam(self):
        # Verificar se a webcam está ligada
        if self.toggle_webcam_button.text() == "Ligar webcam":
            # Ligar a webcam
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 580)
            while self.capture.isOpened():
                ret, frame = self.capture.read()
                if ret:
                    # Converter a imagem para o formato que o Qt aceita
                    height, width, channel = frame.shape
                    step = channel * width
                    image = QImage(frame.data, width, height,
                                   step, QImage.Format.Format_RGB888)
                    pixmap = QPixmap.fromImage(image)
                    self.video_label.setPixmap(pixmap)
                else:
                    print("Can't receive frame (stream end?). Exiting ...")
                    # reiniciar o video
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    break
            self.toggle_webcam_button.setText("Desligar webcam")
        else:
            # Desligar a webcam
            self.capture.release()
            self.video_label.clear()
            self.toggle_webcam_button.setText("Ligar webcam")

    def take_photo(self):
        # Verificar se a webcam está ligada
        if self.toggle_webcam_button.text() == "Desligar webcam":
            # Tirar uma foto
            ret, frame = self.capture.read()
            if ret:
                # Converter a imagem para o formato que o Qt aceita
                image = QImage(frame, frame.shape[1], frame.shape[0],
                               QImage.Format.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap)
                self.image = frame
                # salvar a imagem no disco
                cv2.imwrite("image.jpg", frame)
        else:
            self.show_message_box("Ligue a webcam antes de tirar uma foto!")

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
