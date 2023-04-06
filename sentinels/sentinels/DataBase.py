import psycopg2
from PyQt6.QtWidgets import QMessageBox
import os
from typing import List, Union, Dict, Any, Optional, Tuple

# Database PostgreSQL


class DataBase:
    def __init__(self, port: str, dbname: str, user: str, password: str,
                 host: str = 'localhost'):
        self.dbname: str = dbname
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: str = port
        self.connection: psycopg2.extensions.connection = None

    def connect(self, instance: QMessageBox) -> None:
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                port=self.port,
                password=self.password,
                host=self.host,
            )

        except psycopg2.Error as e:
            if os.path.exists("data.txt"):
                os.remove("data.txt")
            QMessageBox.critical(
                instance, 'Erro',
                'Não foi possível conectar ao banco de '
                'dados. Verifique se o PostgreSQL está '
                'rodando e se as credenciais estão '
                f'corretas. {e}')

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def create(self, instance: QMessageBox, tabela: str, campos: str,
               list_values: List[Union[str, int, float, bool]]
               ) -> Union[int, None]:
        try:
            cur = self.connection.cursor()
            placeholders = ','.join(['%s' for _ in list_values])
            query = f"INSERT INTO {tabela} ({campos}) VALUES ({placeholders})"
            cur.execute(query, list_values)
            return cur.rowcount
        except psycopg2.Error as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao criar registro na tabela {tabela}: {e}')
            return None

    def read(self, instance: QMessageBox, tabela: str,
             campos: Optional[List[str]] = None,
             condicao: Optional[str] = None) -> Optional[List[Tuple]]:
        try:
            cur = self.connection.cursor()
            if campos is None:
                campos_str = '*'
            else:
                campos_str = ','.join(campos)
            if condicao is None:
                cur.execute(f"SELECT {campos_str} FROM {tabela}")
            else:
                query = f"SELECT {campos_str} FROM {tabela} WHERE {condicao}"
                cur.execute(query)
            return cur.fetchall()
        except psycopg2.Error as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao ler registro na tabela {tabela}: {e}')
            return None

    def update(self, instance: QMessageBox, tabela: str,
               valores_dict: Dict[str, Any], condicao: str) -> Optional[int]:
        try:
            cur = self.connection.cursor()
            valores_str = ','.join([f"{campo}=%({campo})s"
                                    for campo in valores_dict.keys()])
            consulta = f"UPDATE {tabela} SET {valores_str} WHERE {condicao}"
            cur.execute(consulta, valores_dict)
            self.connection.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao atualizar registro na tabela {tabela}: {e}')
            return None

    def delete(self, instance: QMessageBox,
               tabela: str, condicao: str) -> Optional[int]:
        try:
            cur = self.connection.cursor()
            cur.execute(f"DELETE FROM {tabela} WHERE {condicao}")
            self.connection.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao deletar registro na tabela {tabela}: {e}')
            return None
