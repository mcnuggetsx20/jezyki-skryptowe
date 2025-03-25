import sys
import datetime
import entries

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
    logs = read_log()
    print(logs[:4])
    print(entries.get_entires_by_extension(logs, '.jpg')[:4])
    print('\n\n')
    print(entries.get_failed_reads(logs, False)[1][:5])
    print('\n\n')
    print(entries.get_entries_by_code(logs, '404')[:5])
    print('\n\n')
    print(entries.get_entries_by_addr(logs, '192.168.202.79')[:5])
