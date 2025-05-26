import sys
import csv
from peewee import MySQLDatabase
from datetime import datetime
from models import db, Stacja, Przejazd

# Dane logowania
MYSQL_USER = 'pythonuser' 
MYSQL_PASSWORD = 'twoje_haslo'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306


def get_or_create_stacja(nazwa):
    stacja, created = Stacja.get_or_create(nazwa=nazwa)
    return stacja

def main():
    if len(sys.argv) != 3:
        print("Użycie: python load_data.py historia.csv baza_danych")
        sys.exit(1)

    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    try:
        # Połącz z bazą
        db.init(
            db_name,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT
        )
        db.connect()
    except:
        print("Podaj poprawną baze")
        return

    # Wczytaj dane z CSV
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    stacja_start = get_or_create_stacja(row[4])
                    stacja_koniec = get_or_create_stacja(row[5])

                    Przejazd.create(
                        uid=int(row[0]),
                        numer_rower=int(row[1]),
                        data_wynajmu=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                        data_zwrotu=datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                        stacja_wynajmy=stacja_start.id,
                        stacja_zwrotu=stacja_koniec.id,
                        czas_trwania=int(row[6])
                    )
                except:
                    print(f"Błąd dla przejazdu UID {row.get('uid')}: {e}")
                    continue

        print("Załadowano dane.")
        db.close()
    except:
        print("Nie poprawny plik")

if __name__ == "__main__":
    main()
