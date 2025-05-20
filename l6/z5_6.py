from pathlib import Path
import re
import os
from typing import List, TypedDict, Optional, Sequence
from datetime import datetime, timedelta
import csv
from z2_3 import TimeSeries
from z4 import ZeroSpikeDetector
from z4 import OutlierDetector
from z4 import ThresholdDetector
from z4 import CompositeValidator
from z4 import SeriesValidator
from z8 import SimpleReporter

class FileInfo(TypedDict):
    filename: Path
    is_loaded: bool
    TimeSeries: List[TimeSeries]


class Measurements:
    def __init__(self, directory : Optional[str]) -> None:
        self.files : dict[tuple[str,str,str], FileInfo] = {}
        self.possibleTimeSeries : Optional[int] = None
        if not directory:
            return
        self.directory : str = directory
        for file in Path(directory).iterdir():
            pattern = re.compile(r'(\d{4})_(\w+)_(\d\w*)\.csv$')
            match = pattern.match(file.name)
            if match:
                year, measurement, frequency = match.groups()
                key = (year, measurement, frequency)
                self.files[key] = {"filename": file,
                                   "is_loaded": False,
                                   "TimeSeries": []}

    def __len__(self) -> int:
        if self.possibleTimeSeries is None:
            self.possibleTimeSeries = 0
            for file_key in self.files:
                with open(self.files[file_key]["filename"], newline='', encoding='utf-8') as csvfile:
                    self.possibleTimeSeries += len(csvfile.readline().split(',')) - 1 
        return self.possibleTimeSeries

    def get_by_parameter(self, param_name: str) -> List[TimeSeries]:
        matching_series : List[TimeSeries] = []
        for file_key in self.files:
            _, measurement, _ = file_key
            if measurement == param_name:
                matching_series.extend(self.load_data(file_key)["TimeSeries"])
        return matching_series

    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        matching_series : List[TimeSeries] = []
        for file_key in self.files:
            year, measurement, frequency = file_key
            file_path = self.files[file_key]["filename"]
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                station_codes = next(reader)[1:]   
                if station_code in station_codes:
                    time_series_data = self.load_data(file_key)["TimeSeries"]
                    for ts in time_series_data:
                        if ts.station_code == station_code:
                            matching_series.append(ts)
        return matching_series

    def load_data(self, file_key : tuple[str,str,str]) -> FileInfo:
        if not self.files[file_key]["is_loaded"]:
            self.files[file_key]["is_loaded"] = True
            with open(self.files[file_key]["filename"], newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                indicators = rows[2][1:]
                station_code = rows[1][1:]
                avereging_time = rows[3][1:]
                unit = rows[4][1:]

                for i in range(len(indicators)):
                    self.files[file_key]["TimeSeries"].append( TimeSeries(indicators[i], station_code[i], avereging_time[i],[],[],unit[i]))

                for row in rows[6:]:
                    try:
                        date = datetime.strptime(row[0], "%m/%d/%y %H:%M")
                    except ValueError:
                        continue 
                    for i in range(1, len(row)):  
                        try:
                            value = float(row[i]) if row[i] != '' else None
                            self.files[file_key]["TimeSeries"][i-1].dates.append(date) 
                            self.files[file_key]["TimeSeries"][i-1].values.append(value) 
                        except ValueError:
                            self.files[file_key]["TimeSeries"][i-1].dates.append(date)
                            self.files[file_key]["TimeSeries"][i-1].values.append(None)          
                    
        return self.files[file_key]
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict[tuple[str, str, str], list[dict[str, Sequence[str]]]]:
        result : dict[tuple[str,str,str], list[dict[str, Sequence[str]]]]= {}

        for file_key in self.files:
            if preload or self.files[file_key]["is_loaded"]:
                anomalies_by_series : List[dict[str,Sequence[str]]] = []

                time_series_list = self.load_data(file_key)["TimeSeries"]

                for ts in time_series_list:
                    anomalies : List[str] = []
                    for validator in validators:
                        anomalies.extend(validator.analyze(ts))

                    series_info = {
                        'station_code': ts.station_code,
                        'indicator_name': ts.indicator_name,
                        'averaging_time': ts.averaging_time,
                        'unit': ts.unit,
                        'anomalies': anomalies
                    }

                    anomalies_by_series.append(series_info) 

                result[file_key] = anomalies_by_series

        return result

import pytest




def create_dummy_series():
    ts = TimeSeries("PM10", "ST01", "1h", [], [], "µg/m3")
    start = datetime(2024, 1, 1, 0, 0)
    ts.dates = [start + timedelta(hours=i) for i in range(4)]
    ts.values = [0, 0.0, 0.0, 0.0] 
    return [ts]


@pytest.mark.parametrize("validator", [
    ZeroSpikeDetector(),
    OutlierDetector(k=2.0),
    SimpleReporter()

])
def test_detect_all_anomalies_with_mock(monkeypatch, validator) -> None:
    ms = Measurements(None)
    dummy_key = ("2024", "PM10", "1h")
    ms.files[dummy_key] = {
        "filename": Path(''),
        "is_loaded": True,
        "TimeSeries": []  
    }

    dummy_ts = create_dummy_series()
    monkeypatch.setattr(ms, "load_data", lambda key: {"TimeSeries": dummy_ts})

    results = ms.detect_all_anomalies([validator], preload=True)

    series = results[dummy_key]

    assert len(series) == 1
    messages = series[0]["anomalies"]
    helper : int = 0
    for i in range (len(dummy_ts)):
        helper = len(validator.analyze(dummy_ts[i]))
    assert len(messages) == helper
    for m in messages:
        assert hasattr(m, "strip") 
        assert len(m.strip()) > 0

    

