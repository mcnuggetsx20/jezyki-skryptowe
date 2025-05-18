#Nr,Kod stacji,Kod międzynarodowy,Nazwa stacji,"Stary Kod stacji 
#(o ile inny od aktualnego)",Data uruchomienia,Data zamknięcia,Typ stacji,Typ obszaru,Rodzaj stacji,Województwo,Miejscowość,Adres,WGS84 φ N,WGS84 λ E
import lib
import pytest


class Station:

    nr: str
    kod_stacji: str
    kod_miedz: str
    nazwa: str
    stary_kod: str
    data_begin: str
    data_end: str
    typ: str
    obszar: str
    rodzaj: str
    woj: str
    miejsc: str
    adres: str
    lon: str
    lat: str
    
    def __init__(
            self,
            nr : str,
            kod_stacji : str,
            kod_miedz : str,
            nazwa : str,
            stary_kod : str,
            data_begin : str,
            data_end : str,
            typ : str,
            obszar : str,
            rodzaj : str,
            woj : str,
            miejsc : str,
            adres : str,
            lon : str,
            lat : str
    )->None:
        for name, value in locals().items():
            if name != 'self':
                setattr(self, name, value)

        return

    def __str__(self) ->str:
        res : str = ''
        for k, v in self.__dict__.items():
            res += f'{k}: {v};'
        return res
    
    def __repr__(self) -> str:
        cls_name : str = self.__class__.__name__
        attrs : str = ', '.join(f"{k}={repr(v)}" for k, v in self.__dict__.items())
        return f"{cls_name}({attrs})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Station):
            return False
        return self.kod_stacji == other.kod_stacji


def test_station_eq():
    s1 = Station('',"ST01",'','','','','','','','','','','','','')
    s2 = Station('',"ST01",'','','','','','','','','','','','','')
    s3 = Station('',"ST02",'','','','','','','','','','','','','')
    assert s1 == s2, "Stacje o tych samych kodach powinny być równe"
    assert s1 != s3, "Stacje o różnych kodach nie powinny być równe"







