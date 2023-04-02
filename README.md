# Alpha's Sentinels

Programa de Visão Computacional para Controle de Acesso

Bibliotecas: (poetry add b_name)
- psycopg2 (PostgreSQL)
- PyQt6 (GUI)
- numpy

Bibliotecas para Processamento de Imagens:
- opencv_contrib_python (cv2)
- scikit-image
- matplotlib

Para rodar o programa em desenvolvimento:
- poetry run python main.py

Para gerar executável:
- poetry add pyinstaller
- poetry run pyinstaller --hidden-import=postgresql --hidden-import=cv2 --hidden-import=uuid --hidden-import=pyzbar --hidden-import=pyzbar.pyzbar --hidden-import=scipy --hidden-import=scipy.spatial --hidden-import=dlib --hidden-import=psycopg2 --hidden-import=qrcode --add-data "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\.venv\Lib\site-packages\pyzbar;pyzbar" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\.venv\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\.venv\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" --add-data "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\icons;icons" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\icons\logo.jpg;icons" --add-data "Tab1;Tab1" --add-data "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\Tab2;Tab2" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\Tab2\dlib_face_recognition_resnet_model_v1.dat;Tab2" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\Tab2\haarcascade_frontalface_default.xml;Tab2" --add-binary "C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\sentinels\Tab2\shape_predictor_68_face_landmarks.dat;Tab2" --add-data "Tab3;Tab3" --add-data "Tab4;Tab4" --add-data "App.py;." --add-data "CreatePostgres.py;." --onefile --noconsole --paths="C:\Codar\python\Processamento de Imagens\bruno\alphas_sentinels-bruno\sentinels\.venv\Lib\site-packages" main.py

