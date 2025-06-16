from lib import filter

def check(sentence):
    return sentence[-1] == '!' or sentence[-1] == '?'

if __name__ == '__main__':
    print(filter(check))
