from lib import filter

def check(sentence):
    word_count = sentence.count(' ') + 1
    return word_count >= 2 and word_count <= 4

if __name__ == '__main__':
    result = filter(check)
    print(result, end='')

