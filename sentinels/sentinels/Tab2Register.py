import psycopg2
import os
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt6.QtGui import QImage, QPixmap


class Tab2Register(QWidget):
    def __init__(self, user_postgresql, password_postgresql):
        super().__init__()
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql
        self.initUI()

    def initUI(self):
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
        cursor.execute("SELECT photo FROM employees WHERE id = %s", (user_id,))
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
