from lib import filter

ANS = ''
def get_longer(new):
    global ANS

    if len(new) > len(ANS):
        ANS = new
    return

def check(sentence):
    get_longer(sentence)
    return True

if __name__ == '__main__':
     filter(check)
     print(ANS)

