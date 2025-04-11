import csv
import re

dates = []
lat_lon = []
stations = []
stations_processed = []
immobile = []
three_piece = []
addr_with_comma = []

with open('stacje.csv' ,'r', encoding='utf-8') as file:
    headers = [i for i in csv.DictReader(file).fieldnames]

    for line in file:
        dates.extend(re.findall(r'\d\d\d\d-\d\d-\d\d', line))

        lat_lon.extend(re.findall(r'\d{2}\.\d{6}', line))

        stations.extend(re.findall(r'\b\w+\b\s*-\s*\b\w+\b', line))

        # WOW
        values = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line.strip()) 
        dt = dict(zip(headers, values))
        if re.findall(r'.*MOB', dt['Kod stacji']):
            if dt['Rodzaj stacji'].lower() != 'mobilna':
                immobile.append(dt)

        if re.findall(r'\b\w+\b\s*-\s*\b\w+\b\s*-\s*\b\w+\b', dt['Nazwa stacji']):
            three_piece.append(dt['Nazwa stacji'])

        if re.findall(r'^.*(?:ul\.|al\.).*,|,.*(?:ul\.|al\.).*$', dt['Nazwa stacji']):
            addr_with_comma.append(dt['Nazwa stacji'])

pl_dict = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
    'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
}

for station in stations:
    processed_line = station.replace(' ', '_')

    processed_line = re.sub(
        r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]',
        lambda x: pl_dict[x.group(0)],
        processed_line
    )

    stations_processed.append(processed_line)
        
if __name__ == '__main__':
    # print(dates)
    # print(lat_lon)
    # print(stations)
    # print(stations_processed)
    # if immobile:
    #     print(f'podp. e): NIE {immobile}')
    # else: 
    #     print('podp. e): TAK')
    # print(three_piece)
    # print(len(addr_with_comma))
    pass



