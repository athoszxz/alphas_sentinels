from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Union, Dict, Any, Optional, Tuple
from PyQt6.QtWidgets import QMessageBox
import os

# Database MongoDB


class DataBase:
    def __init__(self, dbname: str, user: str, password: str,
                 host: str = 'localhost', port: int = 27017):
        self.dbname: str = dbname
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: int = port
        self.connection: Optional[MongoClient] = None

    def connect(self, instance: QMessageBox) -> None:
        try:
            self.connection = MongoClient(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                authSource=self.dbname
            )

        except PyMongoError as e:
            if os.path.exists("data.txt"):
                os.remove("data.txt")
            QMessageBox.critical(
                instance, 'Erro',
                'Não foi possível conectar ao banco de '
                'dados. Verifique se o MongoDB está '
                'rodando e se as credenciais estão '
                f'corretas. {e}')

    def disconnect(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def commit(self) -> None:
        pass

    def close(self) -> None:
        self.disconnect()

    def create(self, instance: QMessageBox, tabela: str, campos: str,
               list_values: List[Union[str, int, float, bool]]
               ) -> Union[int, None]:
        assert self.connection is not None
        try:
            db = self.connection[self.dbname]
            col = db[tabela]
            dict_valores = {}
            for idx, campo in enumerate(campos.split(',')):
                dict_valores[campo] = list_values[idx]
            result = col.insert_one(dict_valores)
            return result.inserted_id
        except PyMongoError as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao criar registro na tabela {tabela}: {e}')
            return None

    def read(self, instance: QMessageBox, tabela: str,
             campos: Optional[List[str]] = None,
             condicao: Optional[str] = None) -> Optional[List[Tuple]]:
        assert self.connection is not None
        try:
            db = self.connection[self.dbname]
            col = db[tabela]
            if campos is None:
                campos = ['*']
            cursor = col.find({}, {campo: 1 for campo in campos})
            return [(tuple(row.values()) if campos == ['*'] else row)
                    for row in cursor]
        except PyMongoError as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao ler registro na tabela {tabela}: {e}')
            return None

    def update(self, instance: QMessageBox, tabela: str,
               valores_dict: Dict[str, Any], condicao: str):
        assert self.connection is not None
        try:
            db = self.connection[self.dbname]
            col = db[tabela]
            col.update_many({"condicao": condicao}, {"$set": valores_dict})
            return col.count_documents
        except PyMongoError as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao atualizar registro na tabela {tabela}: {e}')
            return None

    def delete(self, instance: QMessageBox,
               tabela: str, condicao: str) -> Optional[int]:
        assert self.connection is not None
        try:
            db = self.connection[self.dbname]
            col = db[tabela]
            result = col.delete_many({"condicao": condicao})
            return result.deleted_count
        except PyMongoError as e:
            QMessageBox.critical(
                instance, 'Erro',
                f'Erro ao deletar registro na tabela {tabela}: {e}')
            return 0
