from peewee import *
from datetime import time, datetime

db = MySQLDatabase(None)

class Stacja(Model):
    id = AutoField()
    nazwa = CharField(unique = True)
    class Meta:
        database = db

class Przejazd(Model):
    uid = BigIntegerField(primary_key=True)
    numer_rower = IntegerField()
    data_wynajmu = DateTimeField()
    data_zwrotu = DateTimeField()
    stacja_wynajmy = ForeignKeyField(Stacja, backref= 'wynajmy')
    stacja_zwrotu = ForeignKeyField(Stacja, backref= 'zwroty')
    czas_trwania = IntegerField()
    class Meta:
        database = db
