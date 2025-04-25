import numpy as np
from datetime import datetime, timedelta

class TimeSeries:
    def __init__(self, indicator_name, station_code, averaging_time, dates, values, unit):
        self.indicator_name = indicator_name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self.dates = dates
        self.values = values
        self.unit = unit

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [(self.dates[i], self.values[i]) for i in range(key.start, key.stop, key.step or 1)]
        elif isinstance(key, (int, float)):
            return self.dates[key], self.values[key]
        elif isinstance(key, (datetime, datetime.date)):
            if key in self.dates:
                idx = self.dates.index(key)
                return self.dates[idx], self.values[idx]
            else:
                raise KeyError(f"Data {key} nie istnieje w danych pomiarowych.")
        else:
            raise TypeError(f"Nieobsługiwany typ klucza: {type(key)}")

    @property
    def mean(self):
        # Obliczanie średniej arytmetycznej
        values = [v for v in self.values if v is not None]
        if values:
            return np.mean(values)
        return None

    @property
    def stddev(self):
        # Obliczanie odchylenia standardowego
        values = [v for v in self.values if v is not None]
        if values:
            return np.std(values)
        return None
    
if __name__ == '__main__':
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(5)]
    values = [15.0, 17.3, None, 19.8, 20.1] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    print("Nazwa wskaźnika:", ts.indicator_name)
    print("Średnia:", ts.mean)
    print("Odchylenie standardowe:", ts.stddev)
    print("Wartość z trzeciego pomiaru:", ts[2])
    print("Wartości od 1 do 4:", ts[1:4])
    print("Wartość z daty:", ts[dates[1]])
    print("Wartość z indexu 1:", ts[1])
    print("Wartość z indexu 2:", ts[2])
    print("Slice object", ts[1:3])
    start = datetime(2025, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(10)]
    values = [15.0, 17.3, None, 19.8, 20.1,10.0,20.0,34.0,1.0,20.0] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    print("\n\n")
    print("Nazwa wskaźnika:", ts.indicator_name)
    print("Średnia:", ts.mean)
    print("Odchylenie standardowe:", ts.stddev)
    print("Wartość z trzeciego pomiaru:", ts[2])
    print("Wartości od 1 do 4:", ts[1:4])
    print("Wartość z daty:", ts[dates[1]])
    print("Wartość z indexu 1:", ts[1])
    print("Wartość z indexu 2:", ts[2])
    print("Slice object", ts[1:9:2])

    start = datetime(2025, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(7)]
    values = [15.0, 17.3, None, 19.8, 20.1,1.0,20.0] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    print("\n\n")
    print("Nazwa wskaźnika:", ts.indicator_name)
    print("Średnia:", ts.mean)
    print("Odchylenie standardowe:", ts.stddev)
    print("Wartość z trzeciego pomiaru:", ts[2])
    print("Wartości od 1 do 4:", ts[1:4])
    print("Wartość z daty:", ts[dates[1]])
    print("Wartość z indexu 1:", ts[1])
    print("Wartość z indexu 2:", ts[2])
    print("Slice object", ts[1:5:2])