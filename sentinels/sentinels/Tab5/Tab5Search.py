import psycopg2
import os
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from psycopg2.extras import RealDictCursor


class Tab5Search(QWidget):
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
        # self.image_label.setScaledContents(True)
        # Cria uma imagem padrão
        self.image = QImage("icons/logo.jpg")
        # Exibe a imagem no label
        self.image_label.setPixmap(QPixmap.fromImage(self.image))
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

        # Criar cursor com RealDictCursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Executar a consulta SQL
        query = "SELECT photo from photos WHERE id_employee = %s"
        cursor.execute(query, (user_id,))
        # Pegar a primeira linha como um dicionário
        row = cursor.fetchone()
        if row:
            # Acessar o valor da coluna "photo" diretamente do
            # dicionário retornado
            photo = row["photo"]

            image = QPixmap()
            image.loadFromData(photo)
            # Exibir a imagem no label
            self.image_label.setPixmap(image)
        else:
            # Caso a consulta não retorne nenhuma linha, exibir uma
            # mensagem de erro
            self.show_message_box("Usuário não encontrado.")

    def close_camera(self):
        # Parar a câmera quando a janela for fechada
        self.cap.release()
