import re
import csv
from pathlib import Path
from typing import List, Tuple

def get_addresses(path: Path, city: str) -> List[Tuple[str, str, str, str]]:
    result = []

    with path.open(encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 13:
                continue
            if city.lower() in row[11].lower():
                wojewodztwo = row[10].strip()
                miasto = row[11].strip()
                adres = row[12].strip()

                m = re.match(r'((ul|al|pl)\.\s+[^\d,]+)\s*(\d+)?', adres)
                if m:
                    ulica = m.group(1).strip()
                    numer = m.group(2) or ''
                    result.append((wojewodztwo, miasto, ulica, numer))

    return result

if __name__ == '__main__':
    print(get_addresses(Path('data/stacje.csv'), 'Bogatynia'))
    print('\n')
    print(get_addresses(Path('data/stacje.csv'), 'Wrocław'))
    print('\n')
    print(get_addresses(Path('data/stacje.csv'), 'Jelenia Góra'))