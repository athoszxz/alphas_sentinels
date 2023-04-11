# Alpha's Sentinels

Aplicativo de Visão Computacional para Controle de Acesso.

O aplicativo foi produzido com banco de dados de forma abstrata de forma que pode-se optar em utilizar mongodb ou postgres antes de gerar o executável.

O treinamento do modelo de reconhecimento facial é feito direto no banco de dados.

As técnicas de processamento utilizadas foram: escovamento de pixels, machine learning e análise de pontos faciais.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/11262233/231280792-99191e47-1597-41de-a157-0478c95fd510.gif)

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
- poetry run pyinstaller --hidden-import=postgresql --hidden-import=cv2 --hidden-import=uuid --hidden-import=pyzbar --hidden-import=pyzbar.pyzbar --hidden-import=scipy --hidden-import=scipy.spatial --hidden-import=dlib --hidden-import=psycopg2 --hidden-import=qrcode --add-data "C:\seu-path-para\alphas_sentinels\sentinels\.venv\Lib\site-packages\pyzbar;pyzbar" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\.venv\Lib\site-packages\pyzbar\libiconv.dll;pyzbar" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\.venv\Lib\site-packages\pyzbar\libzbar-64.dll;pyzbar" --add-data "C:\seu-path-para\alphas_sentinels\sentinels\sentinels\icons;icons" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\sentinels\icons\logo.jpg;icons" --add-data "Tab1;Tab1" --add-data "\seu-path-para\alphas_sentinels\sentinels\sentinels\Tab2;Tab2" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\sentinels\Tab2\dlib_face_recognition_resnet_model_v1.dat;Tab2" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\sentinels\Tab2\haarcascade_frontalface_default.xml;Tab2" --add-binary "C:\seu-path-para\alphas_sentinels\sentinels\sentinels\Tab2\shape_predictor_68_face_landmarks.dat;Tab2" --add-data "Tab3;Tab3" --add-data "Tab4;Tab4" --add-data "App.py;." --add-data "CreatePostgres.py;." --onefile --noconsole --paths="\seu-path-para\alphas_sentinels\sentinels\.venv\Lib\site-packages" main.py

