from pyzbar import pyzbar
from scipy.spatial import KDTree
import dlib
import cv2
import pickle
import concurrent.futures

# NÃO MEXE


class QrFaceRecognition:
    def __init__(self):
        self.end = False
        # Carregar apenas uma vez o modelo criado com o pickle
        with open('face_model2.pkl', 'rb') as f:
            self.descriptors = pickle.load(f)

        # Criar apenas uma vez o detector de pontos faciais
        self.sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.facerec = dlib.face_recognition_model_v1(
            'dlib_face_recognition_resnet_model_v1.dat')

        # Inicializar o vídeo da câmera
        self.camera = cv2.VideoCapture(0)

        # Usar um detector de face mais rápido
        self.face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

        # Usar uma janela de exibição menor
        cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Camera", 640, 480)

        # Usar um mecanismo de cache para resultados de detecção
        self.last_dets = []
        self.last_shapes = []
        self.last_descriptors = []

    def __del__(self):
        # desligar a camera
        self.camera.release()
        # fechar todas as janelas
        cv2.destroyAllWindows()

    def capture(self):
        # Loop de captura do QR Code
        while True:
            # Ler o frame
            _, img = self.camera.read()

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
                cv2.imshow("Camera", img)
                cv2.waitKey(3000)
                break

            # Se não encontrou, exibir a mensagem e continuar o loop
            else:
                # Exibir a mensagem com fundo preto e continuar o loop
                cv2.rectangle(img, (20, 20), (440, 80), (0, 0, 0), -1)
                cv2.putText(img, "Capturando Qr Code...", (60, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Camera", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return self.__del__()

        self.face_capture()

    def face_capture(self):
        # Loop de captura de faces
        while True:
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
            cv2.imshow("Camera", img)

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
                        cv2.imshow("Camera", img)
                        cv2.waitKey(6000)
                        return self.capture()

            # Se apertar a tecla 'q', sair do programa
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return self.__del__()

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


# Executar o programa
if __name__ == '__main__':
    app = QrFaceRecognition()
    app.capture()
    cv2.destroyAllWindows()
