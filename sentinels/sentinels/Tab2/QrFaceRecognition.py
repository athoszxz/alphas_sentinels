from pyzbar import pyzbar
from scipy.spatial import KDTree
import dlib
import cv2
# import pickle
import concurrent.futures
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6 import QtCore


class QrFaceRecognition(QWidget):
    def __init__(self, descriptors, sp, facerec, face_cascade, cap):
        super().__init__()
        self.end = False
        # Carregar apenas uma vez o modelo criado com o pickle
        self.descriptors = descriptors

        # Criar apenas uma vez o detector de pontos faciais
        self.sp = sp
        self.facerec = facerec

        # Inicializar o vídeo da câmera
        self.camera = cv2.VideoCapture(0)

        # Usar um detector de face mais rápido
        self.face_cascade = face_cascade

        # # Usar uma janela de exibição menor
        # cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Camera", 640, 480)

        # Usar um mecanismo de cache para resultados de detecção
        self.last_dets = []
        self.last_shapes = []
        self.last_descriptors = []

        self.initUI()

    def initUI(self):
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
        self.video_label.setFixedSize(250, 300)
        # Adiciona bordas à label
        self.video_label.setStyleSheet("border: 1px solid black;")

        # Adiciona a label ao layout
        camera_v_layout.addLayout(cam_power_button_h_layout)
        camera_v_layout.addWidget(self.video_label)

        # Cria um layout vertical para o card de informações do usuário
        user_info_v_layout = QVBoxLayout()
        # Cria uma label para exibir o status de acesso do usuário
        self.user_access_label = QLabel(self)
        # Define o tamanho da label
        self.user_access_label.setFixedSize(150, 50)
        # Adiciona bordas à label
        self.user_access_label.setStyleSheet("border: 1px solid red;")
        # Remove o esaço entre esta label e a próxima
        user_info_v_layout.setSpacing(0)

        # Adiciona a label ao layout
        user_info_v_layout.addWidget(self.user_access_label)

        # Cria uma label para ser o contorno do card
        user_info_label = QLabel(self)
        # Define o tamanho da label
        user_info_label.setFixedSize(250, 300)
        # Adiciona bordas à label
        user_info_label.setStyleSheet("border: 1px solid black;")
        # Adiciona a label ao layout
        user_info_v_layout.addWidget(user_info_label)
        # Adiciona dentro da label, outras labels para exibir as informações
        # do usuário
        self.user_name_label = QLabel(self)
        self.user_name_label.move(10, 10)
        self.user_name_label.setStyleSheet("color: white;")
        self.user_name_label.setParent(user_info_label)
        self.user_name_label.show()
        self.user_last_name_label = QLabel(self)
        self.user_last_name_label.move(10, 40)
        self.user_last_name_label.setStyleSheet("color: white;")
        self.user_last_name_label.setParent(user_info_label)
        self.user_last_name_label.show()
        self.user_cpf_label = QLabel(self)
        self.user_cpf_label.move(10, 70)
        self.user_cpf_label.setStyleSheet("color: white;")
        self.user_cpf_label.setParent(user_info_label)
        self.user_cpf_label.show()
        self.user_birthdate_label = QLabel(self)
        self.user_birthdate_label.move(10, 100)
        self.user_birthdate_label.setStyleSheet("color: white;")
        self.user_birthdate_label.setParent(user_info_label)
        self.user_birthdate_label.show()

        # Adiciona o layout da câmera ao layout principal
        main_h_layout.addLayout(camera_v_layout)
        main_h_layout.addLayout(user_info_v_layout)
        # Define o layout
        self.setLayout(main_h_layout)

        # Inicia o timer para atualizar a imagem da webcam
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.qr_capture)

    def toggle_camera(self):
        if self.camera.isOpened():
            self.camera.release()
            self.timer.stop()
            self.cam_power_button.setText('Iniciar')
            self.video_label.clear()
        else:
            self.camera.open(0)
            self.timer.start(1)
            self.cam_power_button.setText('Parar')

    def __del__(self):
        # desligar a camera
        self.camera.release()
        # fechar todas as janelas
        cv2.destroyAllWindows()

    def get_qimage(self, img):
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

    def qr_capture(self):
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
            # Exibir a mensagem e o conteúdo do QR Code com um fundo preto
            cv2.rectangle(img, (20, 20), (440, 80), (0, 144, 0), -1)
            cv2.putText(img, "QR Code encontrado!", (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            for barcode in barcodes:
                x, y, w, h = barcode.rect
                barcode_info = barcode.data.decode('utf-8')
                cv2.putText(img, barcode_info, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            # Exibir imagem na label
            self.video_label.setPixmap(QPixmap.fromImage(
                self.get_qimage(img)))
            # Atualizar a tela
            # QApplication.processEvents()

            # Aguardar 3 segundos e sair do loop
            cv2.waitKey(3000)
            # Chamar o método para capturar as faces
            # self.camera.release()  # Acho que não precisa
            self.timer.stop()
            self.timer.timeout.disconnect(self.qr_capture)
            self.timer.timeout.connect(self.face_capture)
            self.timer.start(1)
            return

        # Se não encontrou, exibir a mensagem e continuar o loop
        else:
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
                det, label = future.result()
                if label is not None:
                    cv2.rectangle(img, (det[0], det[1]),
                                  (det[0]+det[2], det[1]+det[3]),
                                  (0, 255, 0), 2)
                    cv2.putText(img, label, (500, 500),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)
                    # Exibir imagem na label
                    self.video_label.setPixmap(QPixmap.fromImage(
                        self.get_qimage(img)))
                    cv2.waitKey(3000)
                    self.timer.stop()
                    # desconectar timer
                    self.timer.timeout.disconnect(self.face_capture)
                    # conectar timer para capturar qr code
                    self.timer.timeout.connect(self.qr_capture)
                    self.timer.start(1)

    def process_face(self, img, det, shape, face_descriptor, descriptors):
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
