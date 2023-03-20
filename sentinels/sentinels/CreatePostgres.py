import psycopg2
import os
from PyQt6.QtWidgets import QMessageBox


class CreatePostgres:
    def __init__(self, user_postgresql, password_postgresql):
        self.user_postgresql = user_postgresql
        self.password_postgresql = password_postgresql

    def create(self):
        print("Database 'db_alphas_sentinels_2023_144325' não " +
              "encontrado. Criando...")
        try:
            connection = psycopg2.connect(host="localhost",
                                          database="postgres",
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
        except psycopg2.OperationalError:
            # Verificar se o arquivo data.txt existe e excluí-lo
            if os.path.exists("data.txt"):
                os.remove("data.txt")
                self.show_message_box("Erro ao conectar ao banco de dados " +
                                      "principal 'postgres'")
            return False

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE db_alphas_sentinels_2023_144325")
        connection.close()

        # Criar as tabelas
        try:
            connection = psycopg2.connect(host="localhost",
                                          database="db_alphas_sentinels_2023_"
                                          + "144325",
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
        except psycopg2.OperationalError:
            self.show_message_box("Erro ao conectar ao banco de dados " +
                                  "'db_alphas_sentinels_2023_144325'")
            return False
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, " +
            "first_name VARCHAR(50), last_name VARCHAR(50)," +
            " age INTEGER, photo BYTEA)")
        connection.commit()
        connection.close()
        return True

    def check(self):
        try:
            # Pegar o nome de todos os databases
            connection = psycopg2.connect(host="localhost",
                                          database="postgres",
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
        except psycopg2.OperationalError:
            # Verificar se o arquivo data.txt existe e excluí-lo
            if os.path.exists("data.txt"):
                os.remove("data.txt")
                self.show_message_box("Erro ao conectar ao banco de dados!" +
                                      "\nUsuário e/ou senha incorretos." +
                                      "\nVerifique se o PostgreSQL está" +
                                      " rodando.")

            return False

        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database")
        databases = [database[0] for database in cursor.fetchall()]
        connection.close()
        if "db_alphas_sentinels_2023_144325" not in databases:
            return self.create()
        return True

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
