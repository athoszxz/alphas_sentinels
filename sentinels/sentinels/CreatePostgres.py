import psycopg2
import os
from PyQt6.QtWidgets import QMessageBox
from typing import Union


class CreatePostgres:
    def __init__(self, user_postgresql: str, password_postgresql: str,
                 port: str, host: str):
        self.user_postgresql: str = user_postgresql
        self.password_postgresql: str = password_postgresql
        self.port: str = port
        self.host: str = host

    def connect_database(self, database: str) -> Union[
            bool, psycopg2.extensions.connection]:
        try:
            connection = psycopg2.connect(host=self.host,
                                          port=self.port,
                                          database=database,
                                          user=self.user_postgresql,
                                          password=self.password_postgresql)
            return connection
        except psycopg2.OperationalError:
            if os.path.exists("data.txt"):
                os.remove("data.txt")
            print("Erro ao conectar ao banco de dados " +
                  database)
            return False

    def create(self):
        print("Database 'db_alphas_sentinels_2023_144325' não " +
              "encontrado. Criando...")
        # Criar o banco de dados
        connection = self.connect_database("postgres")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE db_alphas_sentinels_2023_144325")
        connection.close()

        # Criar as tabelas
        connection = self.connect_database("db_alphas_sentinels_2023_144325")
        cursor = connection.cursor()
        # Tabela employees
        cursor.execute(
            " CREATE TABLE IF NOT EXISTS employees ( " +
            " id_employee varchar(36) NOT NULL, " +
            " first_name varchar(50) NOT NULL, " +
            " last_name varchar(50) NOT NULL, " +
            " birth_date DATE NOT NULL," +
            " cpf varchar(11) NOT NULL," +
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
            " profile_photo BOOLEAN NOT NULL DEFAULT 'FALSE',"
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
        connection = self.connect_database("postgres")
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
