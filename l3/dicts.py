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
    d = {
        'a' : 1,
        'b' : 2,
            }
    for k, v in d.items():
        print(k, v)
print_dict_entry_dates(None)
