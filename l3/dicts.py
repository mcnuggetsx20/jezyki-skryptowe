from collections import defaultdict

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
    result = defaultdict(lambda: list())

    for entry in log:
        entry = entry_to_dict(entry)
        result[entry['uid']].append(entry)
        
    return result

def print_dict_entry_dates(dict_log):
    from lib import sort_log

    method_dict = defaultdict(lambda: 0)
    host_dict = defaultdict(lambda: 0)

    for k, v in dict_log.items():
        print(k)

        num_queries = 0
        for dict_entry in v:
            print(dict_entry['host'], dict_entry['uri'])
            method_dict[dict_entry['method']] += 1
            host_dict[dict_entry['host']] += 1

            num_queries += 1

        sorted_by_date = sort_log(v, 'ts')
        print(f'number of queries: {num_queries}')
        print(f'first: {sorted_by_date[0]['ts']} \nlast: {sorted_by_date[-1]['ts']}')
        print()

    method_sum = sum(method_dict.values())
    for k, v in method_dict.items():
        print(f'{k}: {round(v/method_sum * 100, 5)}%')

    print("\nHOSTS:")
    for k, v in host_dict.items():
        print(f'{k}: {v}')



