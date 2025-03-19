from lib import filter

def count(c=[0]):

    # korzystamy z faktu, ze listy sa mutowalne
    # i osiagamy "statyczna" zmienna

    c[0] += 1
    return c[0]

def check(sentence):
    return count() <= 20

result = filter(check)
print(result)
