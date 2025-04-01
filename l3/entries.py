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

def get_failed_reads(list, together=False):
    list_4 = []
    list_5 = []
    for kr in list:
        try:
            if str(kr[10])[0] == '4':
                list_4.append(kr)
            if str(kr[10])[0] == '5':
                if together:
                    list_4.append(kr)
                else:
                    list_5.append(kr)
        except:
            continue
    if together:
        return list_4
    else:
        return list_4, list_5
    
def get_entires_by_extension(log_list, extens):
    logs_with_ext = []
    for kr in log_list:
        if str(kr[9]).endswith(extens):
            logs_with_ext.append(kr)
    return logs_with_ext