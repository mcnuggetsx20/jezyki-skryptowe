def sort_log(log, index):
    if index < 0 or index >= len(log):
        raise Exception('Niepoprawny index!')

    return sorted(log, key=lambda x: x[index])
