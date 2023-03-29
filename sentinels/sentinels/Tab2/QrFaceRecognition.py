from pyzbar import pyzbar
from scipy.spatial import KDTree
import dlib
import cv2
import concurrent.futures
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6 import QtCore
import psycopg2
import os
from typing import List, Dict, Tuple


class QrFaceRecognition(QWidget):
    def __init__(self, descriptors: List, sp: object, facerec: object,
                 face_cascade: object, user_postgresql: str,
                 password_postgresql: str) -> None:
        super().__init__()
        self.user_postgresql: str = user_postgresql
        self.password_postgresql: str = password_postgresql
        self.end: bool = False
        # Carregar apenas uma vez o modelo criado com o pickle
        self.descriptors = descriptors

        # Criar apenas uma vez o detector de pontos faciais
        self.sp: object = sp
        self.facerec: object = facerec

        self.cam_power: bool = False

        # Inicializar o vídeo da câmera
        self.camera: cv2.VideoCapture = cv2.VideoCapture(0)

        # Usar um detector de face mais rápido
        self.face_cascade = face_cascade

        self.all_users_ids: List[str] = []
        self.all_users_names: Dict[str, str] = {}
        self.recognized_user_id: str = ''

        # Usar um mecanismo de cache para resultados de detecção
        self.last_dets: List[object] = []
        self.last_shapes: List[object] = []
        self.last_descriptors: List[object] = []

        self.initUI()

    def initUI(self) -> None:
        # Cria um layout horizontal principal
        main_h_layout = QHBoxLayout()

        # Cria um layout horizontal para o botão de iniciar e parar a câmera
        cam_power_button_h_layout = QHBoxLayout()
        # Cria um botão para iniciar e parar a câmera
        self.cam_power_button = QPushButton('Iniciar', self)
        cam_power_button_h_layout.addWidget(self.cam_power_button)
        self.cam_power_button.clicked.connect(self.toggle_camera)
        # Redimensiona o botão
        self.cam_power_button.setFixedSize(100, 30)

        # Cria um layout vertical para a câmera
        camera_v_layout = QVBoxLayout()
        # Cria uma label para exibir a webcam
        self.video_label = QLabel(self)
        # Define o tamanho da label
        self.video_label.setFixedSize(400, 350)
        # Adiciona bordas à label
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.video_label.setScaledContents(True)

        # Adiciona a label ao layout
        camera_v_layout.addLayout(cam_power_button_h_layout)
        camera_v_layout.addWidget(self.video_label)

        # Cria um layout vertical para o card de informações do usuário
        user_info_v_layout = QVBoxLayout()
        # Cria uma label para exibir o status de acesso do usuário
        self.user_access_label = QLabel(self)
        # Define o tamanho da label
        self.user_access_label.setFixedSize(150, 50)
        # Adiciona um texto à label
        self.user_access_label.setText("Status de acesso")
        # Remove o espaço entre esta label e a próxima
        user_info_v_layout.setSpacing(0)

        # Adiciona a label ao layout
        user_info_v_layout.addWidget(self.user_access_label)

        # Cria uma label para ser o contorno do card
        user_info_label = QLabel(self)
        # Define o tamanho da label
        user_info_label.setFixedSize(300, 450)
        # Adiciona bordas à label
        user_info_label.setStyleSheet("border: 1px solid black;")
        # Adiciona a label ao layout
        user_info_v_layout.addWidget(user_info_label)
        # Centraliza as labels dentro do card

        # Adiciona dentro da label, outras labels para exibir as informações
        # do usuário
        self.user_photo_label = QLabel(self)
        self.user_photo_label.move(70, 10)
        self.user_photo_label.setStyleSheet("border: 1px solid black;")
        self.user_photo_label.setParent(user_info_label)
        self.user_photo_label.setFixedSize(170, 150)
        self.user_photo_label.setScaledContents(True)
        self.user_photo_label.show()

        self.user_name_label = QLabel(self)
        self.user_name_label.move(50, 180)
        self.user_name_label.setStyleSheet("color: black;")
        self.user_name_label.setParent(user_info_label)
        self.user_name_label.setFixedSize(200, 20)
        self.user_name_label.show()

        self.user_cpf_label = QLabel(self)
        self.user_cpf_label.move(50, 210)
        self.user_cpf_label.setStyleSheet("color: black;")
        self.user_cpf_label.setParent(user_info_label)
        self.user_cpf_label.setFixedSize(200, 20)
        self.user_cpf_label.show()

        # self.user_birthdate_label = QLabel(self)
        # self.user_birthdate_label.move(50, 240)
        # self.user_birthdate_label.setStyleSheet("color: black;")
        # self.user_birthdate_label.setParent(user_info_label)
        # self.user_birthdate_label.setFixedSize(200, 20)
        # self.user_birthdate_label.show()

        self.user_qr_code_label = QLabel(self)
        self.user_qr_code_label.move(90, 280)
        self.user_qr_code_label.setStyleSheet("border: 1px solid black;")
        self.user_qr_code_label.setParent(user_info_label)
        self.user_qr_code_label.setFixedSize(120, 120)
        self.user_qr_code_label.setScaledContents(True)
        self.user_qr_code_label.show()

        # Adiciona o layout da câmera ao layout principal
        main_h_layout.addLayout(camera_v_layout)
        main_h_layout.addLayout(user_info_v_layout)
        # Define o layout
        self.setLayout(main_h_layout)

        # Inicia o timer para atualizar a imagem da webcam
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.qr_capture)

    # Método para pegar todos os ids dos usuários
    def get_all_users_ids(self):
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
        cursor.execute("SELECT id_employee from employees")
        self.all_users_ids = cursor.fetchall()

        cursor.execute(
            "SELECT e.id_employee, e.first_name, e.last_name, e.qr_code," +
            " e.cpf, p.photo " +
            "FROM employees e JOIN photos p ON e.id_employee = p.id_employee "
            + "WHERE p.id_photo = (SELECT MIN(id_photo) FROM photos " +
            "WHERE id_employee = e.id_employee)")
        # Transformar a lista de tuplas com 3 elementos
        # em um dicionário onde a chave é o id do usuário
        # e o valor é uma lista com o nome e sobrenome do usuário
        results = cursor.fetchall()
        for row in results:
            id_employee = row[0]
            first_name = row[1]
            last_name = row[2]
            qr_code = row[3]
            cpf = row[4]
            photo = row[5]
            self.all_users_names[id_employee] = (first_name, last_name,
                                                 qr_code, cpf, photo)
        connection.close()
        return True

    # Método para iniciar e parar a câmera
    def toggle_camera(self) -> None:
        self.get_all_users_ids()
        if self.camera.isOpened():
            self.camera.release()
            self.timer.stop()
            self.cam_power = False
            self.cam_power_button.setText('Iniciar')
            self.video_label.clear()
        else:
            self.camera.open(0)
            self.timer.timeout.connect(self.qr_capture)
            self.timer.start(1)
            self.cam_power = True
            self.cam_power_button.setText('Parar')

    def __del__(self) -> None:
        # desligar a camera
        self.camera.release()
        # fechar todas as janelas
        cv2.destroyAllWindows()

    def get_qimage(self, img) -> QImage:
        # Converter a imagem do OpenCV para RGB
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Converter a imagem do OpenCV para QImage
        convert_to_Qt_format = QImage(
            rgb_image.data, img.shape[1], img.shape[0],
            QImage.Format.Format_RGB888)
        # Redimensionar a imagem para caber na label
        p = convert_to_Qt_format.scaled(
            550, 650, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        return p

    def qr_capture(self) -> None:
        # Verificar se a câmera está aberta
        if not self.camera.isOpened():
            return

        # Ler o frame da webcam
        ret, img = self.camera.read()
        if not ret:
            return

        # Detectar o QR Code
        barcodes = pyzbar.decode(img)

        # Se encontrou um QR Code, exibir a mensagem e o conteúdo
        # do QR Code
        if barcodes:
            # Verificar se o id do usuário está cadastrado no banco de dados
            for barcode in barcodes:
                if not self.cam_power:
                    return
                barcode_info = barcode.data.decode('utf-8')
                # Verificar se o id do usuário está cadastrado
                # no banco de dados
                if barcode_info in [tup[0] for tup in self.all_users_ids]:
                    self.recognized_user_id = barcode_info
                    self.user_access_label.setText("Qr Code Reconhecido!\n" +
                                                   "Aguardando reconhecimento"
                                                   + " facial...")
                    self.user_access_label.setStyleSheet("color: blue;")
                    self.user_photo_label.setPixmap(
                        QPixmap.fromImage(
                            QImage.fromData(
                                self.all_users_names
                                [barcode_info][4])))  # type: ignore
                    self.user_photo_label.show()
                    self.user_name_label.setText(
                        self.all_users_names[barcode_info][0] + " " +
                        self.all_users_names[barcode_info][1])
                    self.user_name_label.show()
                    self.user_cpf_label.setText(
                        self.all_users_names[barcode_info][3])
                    self.user_cpf_label.show()
                    self.user_qr_code_label.setPixmap(
                        QPixmap.fromImage(
                            QImage.fromData(
                                self.
                                all_users_names
                                [barcode_info][2])))  # type: ignore

                    # Exibir a mensagem e o conteúdo do QR Code com um
                    # fundo verde
                    cv2.rectangle(img, (20, 20), (440, 80), (0, 144, 0), -1)
                    cv2.putText(img, "QR Code encontrado!", (60, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    for barcode in barcodes:
                        if not self.cam_power:
                            return
                        x, y, w, h = barcode.rect
                        barcode_info = barcode.data.decode('utf-8')
                        cv2.putText(img, self.all_users_names[barcode_info][0],
                                    (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 255, 0), 2)
                    # Exibir imagem na label
                    self.video_label.setPixmap(QPixmap.fromImage(
                        self.get_qimage(img)))

                    # Aguardar 3 segundos e sair do loop
                    cv2.waitKey(3000)
                    # Chamar o método para capturar as faces
                    self.recognized_user_id = barcode_info
                    self.timer.stop()
                    self.timer.timeout.disconnect(self.qr_capture)
                    self.timer.timeout.connect(self.face_capture)
                    self.timer.start(1)
                    return
                else:
                    if not self.cam_power:
                        return
                    self.user_access_label.setText("Acesso negado!")
                    self.user_access_label.setStyleSheet("color: red;")
                    # Exibir a mensagem e o conteúdo do QR Code com um
                    # fundo vermelho
                    cv2.rectangle(img, (20, 20), (440, 80), (0, 0, 144), -1)
                    cv2.putText(img, "QR Code Desconhecido!", (60, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), 2)
                    for barcode in barcodes:
                        if not self.cam_power:
                            return
                        x, y, w, h = barcode.rect
                        barcode_info = barcode.data.decode('utf-8')
                        cv2.putText(img, barcode_info, (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 0, 255), 2)
                    # Exibir imagem na label
                    self.video_label.setPixmap(QPixmap.fromImage(
                        self.get_qimage(img)))

        # Se não encontrou, exibir a mensagem e continuar o loop
        else:
            if not self.cam_power:
                return
            # Exibir a mensagem com fundo preto e continuar o loop
            cv2.rectangle(img, (20, 20), (440, 80), (0, 0, 0), -1)
            cv2.putText(img, "Capturando Qr Code...", (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            self.video_label.setPixmap(QPixmap.fromImage(
                self.get_qimage(img)))

    def face_capture(self):
        # Verificar se a câmera está aberta
        if not self.camera.isOpened():
            return

        # Ler o frame da webcam
        ret, img = self.camera.read()
        if not ret:
            return
        # Ler o frame
        _, img = self.camera.read()
        # Detectar os rostos usando um detector de face mais rápido
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dets = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Armazenar os resultados de detecção e extração de
        # características em cache
        shapes = []
        face_descriptors = []
        for det in dets:
            if not self.cam_power:
                return
            shape = self.sp(img, dlib.rectangle(
                left=det[0], top=det[1], right=det[0]+det[2],
                bottom=det[1]+det[3]))
            face_descriptor = self.facerec.compute_face_descriptor(
                img, shape)
            shapes.append(shape)
            face_descriptors.append(face_descriptor)

        self.last_dets = dets
        self.last_shapes = shapes
        self.last_descriptors = face_descriptors

        # Mostrar o frame
        cv2.rectangle(img, (20, 20), (440, 80), (0, 0, 0), -1)
        cv2.putText(img, "Reconhecendo Rosto...", (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Exibir imagem na label
        self.video_label.setPixmap(QPixmap.fromImage(
            self.get_qimage(img)))

        # Processar os resultados em paralelo usando threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for det, shape, face_descriptor in zip(self.last_dets,
                                                   self.last_shapes,
                                                   self.last_descriptors):
                futures.append(executor.submit(self.process_face, img,
                                               det, shape, face_descriptor,
                                               self.descriptors))

            # Escrever o resultado no frame
            for future in concurrent.futures.as_completed(futures):
                if not self.cam_power:
                    return
                det, label = future.result()
                if label is not None:
                    if label == self.recognized_user_id:
                        cv2.rectangle(img, (det[0], det[1]),
                                      (det[0]+det[2], det[1]+det[3]),
                                      (0, 255, 0), 2)
                        cv2.putText(img, self.all_users_names[label][0],
                                    (det[0], det[1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 255, 0), 2)
                        # Exibir imagem na label
                        self.video_label.setPixmap(QPixmap.fromImage(
                            self.get_qimage(img)))
                        self.user_access_label.setText("Acesso liberado!")
                        self.user_access_label.setStyleSheet("color: green;")
                        cv2.waitKey(3000)
                        self.timer.stop()
                        # desconectar timer
                        self.timer.timeout.disconnect(self.face_capture)
                        # conectar timer para capturar qr code
                        self.timer.timeout.connect(self.qr_capture)
                        self.timer.start(1)
                        return
                    else:
                        cv2.rectangle(img, (det[0], det[1]),
                                      (det[0]+det[2], det[1]+det[3]),
                                      (0, 255, 0), 2)
                        cv2.putText(img, 'Rosto e QR Code Distintos',
                                    (det[0], det[1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 255, 0), 2)
                        # Exibir imagem na label
                        self.video_label.setPixmap(QPixmap.fromImage(
                            self.get_qimage(img)))

    def process_face(self, img, det, shape,
                     face_descriptor, descriptors) -> Tuple:
        # Comparar o descritor facial calculado com os do
        # modelo usando árvore de busca
        dist = []
        tree = KDTree(descriptors['descriptors'])
        dist, index = tree.query([face_descriptor], k=1)

        # Se a distância for menor que 0,6, retornar o label correspondente
        # ao descritor
        if dist[0] < 0.6:
            label = descriptors['labels'][index[0]]
            return det, label

        return det, None

    def show_message_box(self, message) -> None:
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()
