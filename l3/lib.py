import datetime
import sys


def sort_log(log, index):

    try:
        return sorted(log, key=lambda x: x[index])
    except:
        raise Exception("niepoprawny index!")

def read_log():
    logs = []
    for line in sys.stdin:
        try:
            kr = line.split('\t')
            kr = kr[:10] + [kr[14]]
            kr[3] = int (kr[3])
            kr[5] = int(kr[5])
            kr[6] = int(kr[6])
            kr[0] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=float(kr[0]))
            try:
                kr[10] = int(kr[10])
            except:
                kr[10] = -1
            logs.append(tuple(kr))
        except Exception as e:
            print(e)
            continue
    return logs

def read_log_from_path(path):
    logs = []
    with open(path, 'r') as file:
        for line in file:
            try:
                kr = line.split('\t')
                kr = kr[:10] + [kr[14]]
                kr[3] = int (kr[3])
                kr[5] = int(kr[5])
                kr[6] = int(kr[6])
                kr[0] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=float(kr[0]))
                try:
                    kr[10] = int(kr[10])
                except:
                    kr[10] = -1
                logs.append(tuple(kr))
            except Exception as e:
                print(e)
                continue
    return logs
