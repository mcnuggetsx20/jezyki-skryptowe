from z2_3 import TimeSeries
from abc import ABC, abstractmethod
import numpy as np
from typing import List
from datetime import datetime, timedelta
import pytest

class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        pass


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        self.k : float = k
    
    def analyze(self, series: TimeSeries) -> List[str]:
        mean : float | None = series.mean
        stddev : float | None = series.stddev
        if mean is None or stddev is None:
            return []
        
        anomalies : List[str] = []
        for date, value in zip(series.dates, series.values):
            if value is not None and abs(value - mean) > self.k * stddev:
                anomalies.append(f"Outlier detected: {value} at {date} (more than {self.k} standard deviations from mean)")
        return anomalies


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies : List[str] = []
        count : int = 0
        for date, value in zip(series.dates, series.values):
            if value == 0 or value is None:
                count += 1
            else:
                count = 0
            
            if count >= 3:
                anomalies.append(f"Zero spike detected at {date} (3 or more consecutive zeros or missing values)")
        return anomalies



class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold : float = threshold
    
    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies : List[str] = []
        for date, value in zip(series.dates, series.values):
            if value is not None and value > self.threshold:
                anomalies.append(f"Threshold exceeded: {value} at {date} (greater than {self.threshold})")
        return anomalies


class CompositeValidator(SeriesValidator):
    def __init__(self, validators : List[SeriesValidator], mode: str = "OR") ->None:
        self.validators : List[SeriesValidator] = validators
        self.mode : str = mode.upper()

    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies : List[str]=[]

        result : List[str]
        # AND returns only if every validator had result if not empty list
        if self.mode == "AND":
            for validator in self.validators:
                result = validator.analyze(series)
                if result: 
                    anomalies.extend(result)
                else:
                    return []
        # OR returns everything that validators returns
        elif self.mode == "OR":
            for validator in self.validators:
                result = validator.analyze(series)
                anomalies.extend(result)
            return anomalies

        else:
            raise ValueError("Mode must be 'AND' or 'OR'")
        return []

def test_f():
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(5)]
    values = [15.0, 17.3, 1.0, 1000.0, None] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    threshold = ThresholdDetector(10)
    assert 3 == len(threshold.analyze(ts))

def test_e():
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(5)]
    values = [15.0, 17.3, 0, 0, None] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    zero = ZeroSpikeDetector()
    assert 1 == len(zero.analyze(ts))

def test_d():
    indicator_name = "PM10"
    station_code = "ST01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(5)]
    values = [15.0, 17.3, 1.0, 1000.0, None] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    outlier = OutlierDetector(1)
    assert 1 == len(outlier.analyze(ts))

