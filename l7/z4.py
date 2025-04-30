def make_generator(func):
    def generator(bound):
        i = 1
        while(i <= bound):
            yield(func(i))
            i +=1

    return generator

def fib(n):
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a+b
    return a

if __name__ == '__main__':
    fgen = make_generator(fib)
    print([i for i in fgen(10)])

    gen1 = make_generator(lambda n: 2*n)
    gen2 = make_generator(lambda n: 3**n * 2)

    print([i for i in gen1(5)])
    print([i for i in gen2(5)])


