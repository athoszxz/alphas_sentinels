# alphas_sentinels

Desafio Turma Python

Bibliotecas: (poetry add b_name)
*psycopg2 (PostgreSQL)
*PyQt6 (GUI)
*numpy

Bibliotecas para Processamento de Imagens:
*opencv_contrib_python (cv2)
*scikit-image
*matplotlib

Para rodar o programa em desenvolvimento:
*poetry run python main.py

Para gerar executável:
*pip install pyinstaller
*pyinstaller --hidden-import=postgresql --onefile --noconsole main.py
