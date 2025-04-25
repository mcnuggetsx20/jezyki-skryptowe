from pathlib import Path
import re
import os
from typing import List
from datetime import datetime
import csv
from z2 import TimeSeries

class Measurements:
    def __init__(self, directory : str):
        self.directory = directory
        self.files = {}
        self.possibleTimeSeries = None
        for file in Path(directory).iterdir():
            pattern = re.compile(r'(\d{4})_(\w+)_(\d\w*)\.csv$')
            match = pattern.match(file.name)
            if match:
                year, measurement, frequency = match.groups()
                key = (year, measurement, frequency)
                self.files[key] = {"filename":os.path.join(self.directory, file),
                                   "is_loaded": False,
                                   "TimeSeries": []}

    def __len__(self):
        if self.possibleTimeSeries is None:
            self.possibleTimeSeries = 0
            for file_key in self.files:
                with open(self.files[file_key]["filename"], newline='', encoding='utf-8') as csvfile:
                    self.possibleTimeSeries += len(csvfile.readline().split(',')) - 1 
        return self.possibleTimeSeries

    def get_by_parameter(self, param_name: str) -> List:
        matching_series = []
        for file_key in self.files:
            _, measurement, _ = file_key
            if measurement == param_name:
                matching_series.append(self.load_data(file_key)["TimeSeries"])
        return matching_series

    def get_by_station(self, station_code: str) -> List:
        matching_series = []
        for file_key in self.files:
            year, measurement, frequency = file_key
            file_path = self.files[file_key]
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  
                if station_code in headers:
                    matching_series.append(self.load_data(file_key)["TimeSeries"])
        return matching_series

    def load_data(self, file_key) -> List[tuple]:
        if not self.files[file_key]["is_loaded"]:
            self.files[file_key]["is_loaded"] = True
            with open(self.file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                indicators = rows[2][1:]
                station_code = rows[1][1:]
                avereging_time = rows[3][1:]
                unit = rows[4][1:]

                for i in range(len(indicators)):
                    self.files[file_key]["TimeSeries"].append( TimeSeries(indicators[i], station_code[i], avereging_time[i],[],[],unit[i]))

                for row in rows[6:]:
                    date = datetime.strptime(row[0], "%m/%d/%y %H:%M")
                    for i in range(1, len(row)):  
                        try:
                            value = float(row[i]) if row[i] != '' else None
                            self.files[file_key]["TimeSeries"][i-1].dates.append(date) 
                            self.files[file_key]["TimeSeries"][i-1].values.append(value) 
                        except ValueError:
                            self.files[file_key]["TimeSeries"][i-1].dates.append(date)
                            self.files[file_key]["TimeSeries"][i-1].values.append(None)          
                    
        return self.files[file_key]
    
    def detect_all_anomalies(self, validators: list, preload: bool = False) -> dict:
        result = {}

        for file_key in self.files:
            if preload or self.files[file_key]["is_loaded"]:
                anomalies_by_series = []

                time_series_list = self.load_data(file_key)["TimeSeries"]

                for ts in time_series_list:
                    anomalies = []
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


