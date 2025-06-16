import sys
import pymysql
from peewee import MySQLDatabase
from models import db, Stacja, Przejazd

# Dane logowania do MySQL — dostosuj je do swojego systemu!
MYSQL_USER = 'pythonuser' 
MYSQL_PASSWORD = 'twoje_haslo'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306

def create_mysql_database(db_name):
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    connection.close()

def main():
    if len(sys.argv) != 2:
        print("Użycie: python create_database.py NAZWA_BAZY")
        sys.exit(1)

    db_name = sys.argv[1]

    # 1. Utwórz bazę danych
    create_mysql_database(db_name)

    # 2. Przypisz bazę do modeli
    db.init(
        db_name,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT
    )

    # 3. Połącz i utwórz tabele
    db.connect()
    db.create_tables([Stacja, Przejazd])
    db.close()

    print(f"Baza danych '{db_name}' została utworzona z tabelami.")

if __name__ == "__main__":
    main()
