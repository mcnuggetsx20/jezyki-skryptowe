#Nr,Kod stacji,Kod międzynarodowy,Nazwa stacji,"Stary Kod stacji 
#(o ile inny od aktualnego)",Data uruchomienia,Data zamknięcia,Typ stacji,Typ obszaru,Rodzaj stacji,Województwo,Miejscowość,Adres,WGS84 φ N,WGS84 λ E
import lib
class Station:
    def __init__(
            self,
            nr,
            kod_stacji,
            kod_miedz,
            nazwa,
            stary_kod,
            data_begin,
            data_end,
            typ,
            obszar,
            rodzaj,
            woj,
            miejsc,
            adres,
            lon,
            lat
    ):
        for name, value in locals().items():
            if name != 'self':
                setattr(self, name, value)

        return

    def __str__(self):
        res = ''
        for k, v in self.__dict__.items():
            res += f'{k}: {v};'
        return res
    
    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = ', '.join(f"{k}={repr(v)}" for k, v in self.__dict__.items())
        return f"{cls_name}({attrs})"
    
    def __eq__(self, other):
        return self.kod_stacji == other.kod_stacji

if __name__ == '__main__':
    filedata = lib.read_stations()
    print(filedata[3])
    
    print(filedata[4])
    args1 = lib.split_line(filedata[3])
    args2 = lib.split_line(filedata[4])

    st1 = Station(*args1)
    st2 = Station(*args2)
    print(st1 == st2)
    st2.kod_stacji = st1.kod_stacji
    print(st1 == st2)
    print('\n\n')
    print(str(st1))
    print('\n\n')
    print(str(st2))
    print('\n\n')
    print(repr(st1))
    print('\n\n')
    print(repr(st2))





