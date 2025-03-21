from lib import filter

def count(c=[0]):

    # korzystamy z faktu, ze listy sa mutowalne
    # i osiagamy "statyczna" zmienna

    c[0] += 1
    return c[0]

def check(_):
    return count() <= 20

if __name__ == '__main__':
    result = filter(check)
    print(result)
