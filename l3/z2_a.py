import sys
import datetime
import entries
import dicts
import lib

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
                kr[10] = None
            logs.append(tuple(kr))
        except Exception as e:
            print(e)
            continue
    return logs

if __name__ == '__main__':
    logs = read_log()
    print(dicts.print_dict_entry_dates(dicts.log_to_dict(logs)))
    # print(dicts.entry_to_dict(logs[2]))
    print('\n\n')
    # print(dicts.entry_to_dict(logs[3]))
    # print(entries.get_entires_by_extension(logs, '.jpg')[:4])
    # print('\n\n')
    # print(entries.get_failed_reads(logs, False)[1][:5])
    # print('\n\n')
    # print(entries.get_entries_by_code(logs, '404')[:5])
    # print('\n\n')
    # print(entries.get_entries_by_addr(logs, '192.168.202.79')[:5])

    # dicts.print_dict_entry_dates(dicts.log_to_dict(logs))
