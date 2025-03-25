import sys
import datetime
import lib

def read_log():
    logs = []
    for line in sys.stdin:
        try:
            kr = line.split('\t')[:10]
            kr[3] = int (kr[3])
            kr[5] = int(kr[5])
            kr[6] = int(kr[6])
            kr[0] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=float(kr[0]))
            
            logs.append(kr)
        except:
            continue
    return logs[:10]

if __name__ == '__main__':
    # print(lib.sort_log(read_log(), 0))
    result = lib.sort_log(read_log(), 3)
    for i in result:
        print(i)

