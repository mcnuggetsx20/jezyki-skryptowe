def sort_log(log, index):

    try:
        return sorted(log, key=lambda x: x[index])
    except:
        raise Exception("niepoprawny index!")
