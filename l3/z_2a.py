import sys
import datetime

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
            logs.append(kr)
        except Exception as e:
            continue
    return logs

if __name__ == '__main__':
    print(read_log())