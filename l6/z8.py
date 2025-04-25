from z2_3 import TimeSeries
from typing import List
from z2_3 import TimeSeries
from z4 import ZeroSpikeDetector
from z4 import OutlierDetector
from z4 import ThresholdDetector
from z4 import CompositeValidator
from datetime import datetime, timedelta

class SimpleReporter:
    def analyze(self, series: TimeSeries) -> List[str]:
        return [f"Info: {series.indicator_name} at {series.station_code} has mean = {series.mean:.2f}"]
    
if __name__ == '__main__':
    analyzer = []
    analyzer.append(ZeroSpikeDetector())
    analyzer.append(ZeroSpikeDetector())
    analyzer.append(ThresholdDetector(10))
    analyzer.append(SimpleReporter())
    analyzer.append(OutlierDetector(1))
    indicator_name = "PM10"
    station_code = "STACJA01"
    averaging_time = "1h"
    unit = "µg/m3"
    start = datetime(2024, 1, 1, 0, 0)
    dates = [start + timedelta(hours=i) for i in range(5)]
    values = [15.0, 17.3, None, None, None] 
    ts = TimeSeries(indicator_name, station_code, averaging_time, dates, values, unit)
    for analiz in analyzer:
        print(analiz.analyze(ts))
    analyzer.append(SimpleReporter())
    analyzer.append(SimpleReporter())
    print('\n')
    for analiz in analyzer:
        print(analiz.analyze(ts))
    analyzer.append(SimpleReporter())
    analyzer.append(SimpleReporter())
    print('\n')
    for analiz in analyzer:
        print(analiz.analyze(ts))