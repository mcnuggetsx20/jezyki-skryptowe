from collections import defaultdict

def get_keys():
    return [
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
        'status_code',
    ]

def entry_to_dict(entry):
    keys = get_keys()
    return dict(zip(keys, entry))

def log_to_dict_list(log):
    result = list()

    for entry in log:
        result.append(entry_to_dict(entry))
        
    return result

def log_to_dict(log):
    result = defaultdict(lambda: list())

    for entry in log:
        print(entry)
        entry = entry_to_dict(entry)
        result[entry['uid']].append(entry)
        
    return result

def print_dict_entry_dates(dict_log):
    from lib import sort_log

    method_dict = defaultdict(lambda: 0)
    host_dict = defaultdict(lambda: 0)
    code_dict = {
            '2xx' : 0,
            'other' : 0,
            }

    for k, v in dict_log.items():
        print(k)

        num_queries = 0
        for dict_entry in v:
            print(dict_entry['host'], dict_entry['uri'])

            method_dict[dict_entry['method']] += 1
            host_dict[dict_entry['host']] += 1
            
            code = str(dict_entry['status_code'])
            index = '2xx' if (code[0]=='2' and len(code)==3) else 'other'
            code_dict[index]+= 1

            num_queries += 1

        sorted_by_date = sort_log(v, 'ts')
        print(f'number of queries: {num_queries}')
        print(f'first: {sorted_by_date[0]["ts"]} \nlast: {sorted_by_date[-1]["ts"]}')
        print()

    method_sum = sum(method_dict.values())
    for k, v in method_dict.items():
        print(f'{k}: {round(v/method_sum * 100, 5)}%')

    print("\nHOSTS:")
    for k, v in host_dict.items():
        print(f'{k}: {v}')

    code_sum = sum(code_dict.values())
    print(f"\n2xx/other: {code_dict['2xx'] / code_sum}")



