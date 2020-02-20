import mysql.connector
import config
from mysql.connector import errorcode
import mySQL_queries as sql_q


def interact_with_db(book_data):
    try:
        cnx = mysql.connector.connect(user=config.username_db, password=config.password_db,
                                      host='127.0.0.1',
                                      database='storytel')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()

        try:
            cursor.executemany(sql_q.add_book, book_data)

        except mysql.connector.errors.IntegrityError as err:
            print(err)

        cnx.commit()
        cursor.close()
        cnx.close()


