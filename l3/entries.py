def get_entries_by_addr(list , addr):
    logs_with_ip = []
    for kr in list:
        if kr[2] == addr:
            logs_with_ip.append(kr)
    return logs_with_ip

def get_entries_by_code(list, code):
    logs_with_code = []
    for kr in list:
        if kr[10] == code:
            logs_with_code.append(kr)
    return logs_with_code