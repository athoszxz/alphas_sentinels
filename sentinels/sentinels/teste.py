import psycopg2

# Verificar se consigo uma conexão com o postgresql dentro do docker
try:
    connection = psycopg2.connect(user='postgres',
                                  password='25063636',
                                  host="localhost",
                                  port="5433",
                                  database="postgres")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
