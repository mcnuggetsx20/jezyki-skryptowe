import re
from pathlib import Path
from typing import Dict, Tuple

def group_measurement_files_by_key(path: Path) -> Dict[Tuple[str, str, str], Path]:
    pattern = re.compile(r'(\d{4})_(\w+)_(\d\w*)\.csv$')
    grouped_files = {}

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                year, measurement, frequency = match.groups()
                grouped_files[(year, measurement, frequency)] = Path(file)

    return grouped_files

if __name__ == '__main__':
    print(group_measurement_files_by_key(Path('data/measurements')))
