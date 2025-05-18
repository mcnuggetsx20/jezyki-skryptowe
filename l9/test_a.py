import pytest
from ..l6.z1 import Station
import ..l6.lib as lib

def eq_station_test():
    filedata = lib.read_stations()
    print(filedata[3])
    
    print(filedata[4])
    args1 = lib.split_line(filedata[3])
    args2 = lib.split_line(filedata[4])

    st1 = Station(*args1)
    st2 = Station(*args2)
    print(st1 == st2)
    st2.kod_stacji = st1.kod_stacji
    print(st1 == st2, end = 4 * '\n')