from lib import filter

TAB = list()
def get_lengths(sentence):
    global TAB

    TAB.append(sentence)
    return True

if __name__ == '__main__':
    filter(get_lengths)

    lengths = sorted([len(i) for i in TAB])
    for i in TAB:
        if len(i) >= lengths[len(lengths)* 3 // 4]:
            print(i)
