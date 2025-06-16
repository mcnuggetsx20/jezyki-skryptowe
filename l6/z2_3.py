import numpy as np
from datetime import datetime, timedelta, date
from typing import Optional, Union
import pytest

class TimeSeries:
    def __init__(self, indicator_name : str, station_code : str, averaging_time : str, dates : list[datetime], values : list [Optional[float]], unit : str) -> None:
        self.indicator_name : str = indicator_name
        self.station_code :str = station_code
        self.averaging_time : str = averaging_time
        self.dates : list[datetime] = dates
        self.values : list [Optional[float]] = values
        self.unit : str = unit



    def __getitem__(self, key: Union[int, slice, datetime, date]) -> tuple[datetime, float | None] | list[tuple[datetime, float | None]]:
        if isinstance(key, slice):
            return [(self.dates[i], self.values[i]) for i in range(*key.indices(len(self.dates)))]
        elif isinstance(key, int):
            return self.dates[key], self.values[key]
        elif isinstance(key, (datetime, date)):
            if isinstance(key, date) and not isinstance(key, datetime):
                key = datetime.combine(key, datetime.min.time())
            if key in self.dates:
                idx : int  = self.dates.index(key)
                return self.dates[idx], self.values[idx]
            else:
                raise KeyError(f"Data {key} nie istnieje w danych pomiarowych.")
        else:
            raise TypeError(f"Nieobsługiwany typ klucza: {type(key)}")


    @property
    def mean(self) -> float | None:
        # Obliczanie średniej arytmetycznej
        values : list[float]= [v for v in self.values if v is not None]
        if values:
            return float(np.mean(values))
        return None

    @property
    def stddev(self) -> float | None:
        # Obliczanie odchylenia standardowego
        values : list[float] = [v for v in self.values if v is not None]
        if values:
            return float(np.std(values))
        return None
    
def time_series():
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(6)]
    values = [10.0,20.0,30.0,40.0,50.0,60.0] 
    return TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)

def time_series_with_none():
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(7)]
    values = [10.0,20.0,30.0,40.0,50.0,60.0, None] 
    return TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)

def test_b_1():
    ts = time_series()
    value = ts[0]
    assert (datetime(2024,1,1,0,0) , 10.0) == value, "Blad"

def test_b_2():
    ts = time_series()
    value = ts[0:2]
    assert value == [(datetime(2024,1,1,0,0),10.0),(datetime(2024,1,1,1,0),20.0)]

def test_b_3():
    ts = time_series()
    value = ts[datetime(2024,1,1,0,0)]
    assert value == (datetime(2024,1,1,0,0), 10.0)

def test_b_4():
    ts = time_series()
    with pytest.raises(KeyError):
        ts[datetime(2024,2,1,0,0)]

def test_c_1():
    ts = time_series()
    assert ts.mean == 35.0
    assert int(ts.stddev) == 17

def test_c_2():
    ts = time_series_with_none()
    assert ts.mean == 35.0
    assert int(ts.stddev) == 17
