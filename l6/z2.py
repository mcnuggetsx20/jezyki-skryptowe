import numpy as np
from datetime import datetime

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
