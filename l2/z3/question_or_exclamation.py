from lib import filter

def check(sentence):
    return sentence[-1] == '!' or sentence[-1] == '?'

# filter(check)
print(filter(check))
