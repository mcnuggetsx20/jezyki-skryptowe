import sys
import csv
from peewee import MySQLDatabase
from datetime import datetime
from models import db, Stacja, Przejazd


MYSQL_USER = 'pythonuser' 
MYSQL_PASSWORD = 'twoje_haslo'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306

def first_choice():
    stacja_name = input("Podaj nazwe stacji: ")
    stacja = Stacja.get(nazwa=stacja_name)
    try:
        stacja = Stacja.get(nazwa=stacja_name)
    except:
        print("Nie ma takiej stacji")
        return
    wynajmy = stacja.wynajmy
    ile = 0
    czas = 0
    if len(wynajmy) == 0:
        print('Brak danych')
        return
    for wynajem in wynajmy:
        ile += 1
        czas += wynajem.czas_trwania
    print (czas/ile)

def second_choice():
    stacja_name = input("Podaj nazwe stacji: ")
    try:
        stacja = Stacja.get(nazwa=stacja_name)
    except:
        print("Nie ma takiej stacji")
        return
    wynajmy = stacja.zwroty
    ile = 0
    czas = 0
    if len(wynajmy) == 0:
        print('Brak danych')
        return
    
    for wynajem in wynajmy:
        ile += 1
        czas += wynajem.czas_trwania
    print (czas/ile)

def third_choice():
    stacja_name = input("Podaj nazwe stacji: ")
    try:
        stacja = Stacja.get(nazwa=stacja_name)
    except:
        print("Nie ma takiej stacji")
        return
    wynajmy = stacja.zwroty

    wynajmy = stacja.zwroty

    if len(wynajmy) == 0:
        print("0")
        return
    rowery = set()
    for wynajem in wynajmy:
        rowery.add(wynajem.numer_rower)
    print(len(rowery))

def fourth_choice():
    id_bike = input("Podaj id roweru: ")

    try:
        przejazd = (Przejazd
                    .select()
                    .where(Przejazd.numer_rower == id_bike)
                    .order_by(Przejazd.data_zwrotu.desc())
                    .get())
        print("Stacja zwrotu:", przejazd.stacja_zwrotu.nazwa)
    except Przejazd.DoesNotExist:
        print("Nie ma takiego roweru")

def main_loop():
    if len(sys.argv) != 2:
        print("Użycie: python select_data.py baza_danych")
        sys.exit(1)


    db.init(
        sys.argv[1],
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT
    )
    db.connect()

    choice = '1'

    while(choice != '0'):
        print("---------------MENU------------")
        print("'1'-sredni czas trwania przejazdu rozpoczetej na danej stacji")
        print("'2'-sredni czas trwania skonczonego rozpoczetej na danej stacji")
        print("'3'-liczbe roznych rowerow na danej stacji")
        print("'4'-gdzie aktualnie jest rower")
        choice = input("Twoj wybor ")

        if(choice == '1'):
            first_choice()
        if(choice == '2'):
            second_choice()
        if(choice == '3'):
            third_choice()
        if(choice == '4'):
            fourth_choice()

if __name__ == '__main__':
    print('kupa')
    main_loop()


