from sys import stdin

if __name__ == '__main__':
    file = ''
    line_idx = 0
    char_idx = 0
    start = 0
    last_temp = ''

    for line in stdin:
        temp = line.strip()
        temp = temp + '\n' if temp else line

        if line_idx > 0 and line_idx < 10 and not start:
            if temp == last_temp =='\n':
                start = char_idx

        file += temp
        last_temp = temp

        line_idx += 1
        char_idx += len(temp)

    while start < len(file) and file[start] == '\n': start += 1
    stop = file.find('-----')
    print(file[start:stop])

