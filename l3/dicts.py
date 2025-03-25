def entry_to_dict(entry):
    keys = [
        'ts',
        'uid',
        'id.orig_h',
        'id.orig_p',
        'id.resp_h',
        'id.resp_p',
        'trans_depth',
        'method',
        'host',
        'uri',
    ]
    return dict(zip(keys, entry))

def log_to_dict(log):
    from collections import defaultdict
    result = defaultdict(lambda: list())

    for entry in log:
        entry = entry_to_dict(entry)
        result[entry['uid']].append(entry)
        
    return result

def print_dict_entry_dates(dict_log):
    from lib import sort_log

    for k, v in dict_log.items():
        print(k)

        num_queries = 0
        tuple_log = list()
        for dict_entry in v:
            print(dict_entry['host'], dict_entry['uri'])
            tuple_log.append(tuple(dict_entry.values()))

            num_queries += 1

        sorted_by_date = sort_log(tuple_log, 0)
        print(f'number of queries: {num_queries}')
        print(f'first: {sorted_by_date[0][0]} \nlast: {sorted_by_date[-1][0]}')
        print()


