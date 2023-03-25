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
        # Tabela employees
        cursor.execute(
            " CREATE TABLE IF NOT EXISTS employees ( " +
            " id_employee varchar(36) NOT NULL, " +
            " first_name varchar(50) NOT NULL, " +
            " last_name varchar(50) NOT NULL, " +
            " birth_date DATE NOT NULL," +
            " qr_code bytea NOT NULL," +
            " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," +
            " deleted_at TIMESTAMP," +
            " is_active BOOLEAN NOT NULL DEFAULT 'TRUE'," +
            "CONSTRAINT employees_pk PRIMARY KEY (id_employee)" +
            ") WITH (" +
            "  OIDS=FALSE " +
            ");")
        # Tabela photos
        cursor.execute(
            " CREATE TABLE IF NOT EXISTS photos ( " +
            " id_photo varchar(36) NOT NULL, " +
            " id_employee varchar(36) NOT NULL," +
            " photo bytea NOT NULL, " +
            " created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," +
            " changed_at TIMESTAMP," +
            " deleted_at TIMESTAMP," +
            "CONSTRAINT photos_pk PRIMARY KEY (id_photo, id_employee)" +
            ") WITH (" +
            "  OIDS=FALSE " +
            ");")
        # Tabela attendances
        cursor.execute(
            " CREATE TABLE IF NOT EXISTS attendances ( " +
            " id_attendance varchar(36) NOT NULL, " +
            " id_employee varchar(36) NOT NULL," +
            " check_in TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," +
            " valid BOOLEAN NOT NULL," +
            " qr_code bytea NOT NULL," +
            " face_photo bytea NOT NULL," +
            "CONSTRAINT attendance_pk PRIMARY KEY (id_attendance, id_employee)"
            + ") WITH (" +
            "  OIDS=FALSE " +
            ");")
        # CONSTRAINTS
        cursor.execute(
            "ALTER TABLE photos ADD CONSTRAINT photos_fk0 FOREIGN KEY" +
            " (id_employee) REFERENCES employees(id_employee);")
        cursor.execute(
            "ALTER TABLE attendances ADD CONSTRAINT attendance_fk0 FOREIGN " +
            "KEY (id_employee) REFERENCES employees(id_employee);")

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
