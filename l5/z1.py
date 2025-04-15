import csv
import os

def parse_metadane(path):
    stacje = {}
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kod = row["Kod stacji"]

            row["WGS84 φ N"] = float(row["WGS84 φ N"])
            row["WGS84 λ E"] = float(row["WGS84 λ E"])

            row["pomiar"] = {}
            stacje[kod] = row
    return stacje


def parse_pomiary(path, stacje):
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

        kody_stacji = rows[1][1:]
        wskazniki = rows[2][1:]
        czasy_srednie = rows[3][1:]
        jednostki = rows[4][1:]

        for i, kod in enumerate(kody_stacji):
            if kod not in stacje:
                continue 
            stacje[kod]["pomiar"][wskazniki[i]] = {
                "jednostka": jednostki[i],
                "czas_sredni": czasy_srednie[i],
                "dane": []
            }

        for row in rows[4:]:
            for i, val in enumerate(row[1:]):
                if kody_stacji[i] not in stacje or wskazniki[i] not in stacje[kody_stacji[i]]["pomiar"]:
                    continue
                try:
                    wartosc = float(val)
                except:
                    continue 
                stacje[kody_stacji[i]]["pomiar"][wskazniki[i]]["dane"].append({
                    "data": row[0],
                    "wartosc": wartosc
                })

def parse_dane(metadane_path, folder_pomiarów):
    stacje = parse_metadane(metadane_path)
    for filename in os.listdir(folder_pomiarów):
        if filename.endswith(".csv"):
            parse_pomiary(os.path.join(folder_pomiarów, filename), stacje)
    return stacje

if __name__ == '__main__':
    dane = parse_dane('data/stacje.csv', 'data/measurements/')
    print(dane['DsBialka'])
    print(dane['DsBielGrot'])
    print(dane['DsBogatFrancMOB'])