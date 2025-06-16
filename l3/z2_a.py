import sys
import datetime
import entries
import dicts
import lib


if __name__ == '__main__':
    logs = lib.read_log()
    print(lib.sort_log(logs,10))
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
