from lib import filter

def check(sentence):
    i = sentence.find(' ')
    last = sentence[:i].lower()
    sentence = sentence[i+1:]

    while len(sentence):
        i = sentence.find(' ')
        temp = sentence[:i].lower()
        # print([last, temp])

        for j in range(min(len(temp), len(last))):
            if ord(last[j]) > ord(temp[j]):
                return False
            elif ord(last[j]) < ord(temp[j]):
                break

        sentence = sentence[i+1:]
        last = temp

        if i == -1: break
    return True


if __name__ == '__main__':
    print(filter(check))
    # filter(check)



