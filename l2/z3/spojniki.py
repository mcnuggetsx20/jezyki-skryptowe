from lib import filter

def check(sentence):
    ans =   min(1, sentence.count(' ale ')) +\
            min(1, sentence.count(' oraz ')) +\
            min(1, sentence.count(' że ')) +\
            min(1, sentence.count(' lub ')) +\
            min(1, sentence.count(' i '))

    return ans >=2

if __name__ == '__main__':
    print(filter(check))
