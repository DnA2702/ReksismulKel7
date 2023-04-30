import psycopg2
from psycopg2 import Error
import datetime


def presensi(nim):
    current_time = datetime.datetime.now()
    database_time = str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)
    try:
        # Konek ke database
        connection = psycopg2.connect(user="xcyttpkm",
                                    password="JH9CbucFcNO_RJBakeEBiIbIT3yKzAuz",
                                    host="arjuna.db.elephantsql.com",
                                    port="5432",
                                    database="xcyttpkm")

        # Buat kursor operasional database
        cursor = connection.cursor()
        # Ambil data
        cursor.execute("SELECT * FROM absensi") 
        record = cursor.fetchall()
        for r in record:
            print (r)
        # Presensi
        cursor.execute(("UPDATE absensi Set status = 'true' WHERE nim = %s and tanggal = %s"),(str(nim),database_time))
        connection.commit()
        # Ambil data setelah presensi
        print ("---------- Setelah Presensi Dilakukan -----------")
        cursor.execute("SELECT * FROM absensi")
        record = cursor.fetchall()
        for r in record:
            print (r)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getnama(nim):
    try:
        # Konek ke database
        connection = psycopg2.connect(user="xcyttpkm",
                                    password="JH9CbucFcNO_RJBakeEBiIbIT3yKzAuz",
                                    host="arjuna.db.elephantsql.com",
                                    port="5432",
                                    database="xcyttpkm")

        # Buat kursor operasional database
        cursor = connection.cursor()
        # Ambil data
        cursor.execute(("SELECT nama FROM absensi WHERE nim = %s LIMIT 1"),(str(nim),))
        record = cursor.fetchone() 
        return(str(record[0]))
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def validatenim(nim):
    try:
        # Konek ke database
        connection = psycopg2.connect(user="xcyttpkm",
                                    password="JH9CbucFcNO_RJBakeEBiIbIT3yKzAuz",
                                    host="arjuna.db.elephantsql.com",
                                    port="5432",
                                    database="xcyttpkm")

        # Buat kursor operasional database
        cursor = connection.cursor()
        # Ambil data
        cursor.execute(("SELECT nim FROM absensi WHERE nim = %s"),(str(nim),))
        record = cursor.fetchone() 
        if (str(record) != "None" ):
            return(True)
        else:
            return(False)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
