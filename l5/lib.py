import re

def read_stations() -> list:
    split_pattern = r'\n(?=(?:[^"]*"[^"]*")*[^"]*$)'

    file = open('data/stacje.csv', 'r')
    filedata = file.read().strip()
    filedata = re.split(split_pattern, filedata)
    file.close()
    return filedata

def get_measurements(quan, freq) -> list:
    from os import listdir, path

    folder = 'data/measurements'
    files = []
    for i in listdir(folder):
        temp = re.split(r'_|\.', i)
        if len(temp) != 4: continue
        if quan in temp[1] and freq == temp[2]:
            files.append(path.join(folder, i))

    return files


