from functools import lru_cache

def make_generator(func):
    def generator(bound):
        i = 1
        while(i <= bound):
            yield(func(i))
            i +=1

    return generator

def make_generator_mem(func):

    mem_func = lru_cache()(func)

    gen = make_generator(mem_func)
    return lambda bound: gen(bound)

def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    from time import time
    fgen = make_generator(fib)
    start = time()
    print([i for i in fgen(25)])
    print(time()-start)

    gen1 = make_generator(lambda n: 2*n)
    gen2 = make_generator(lambda n: 3**n * 2)
    gen3 = make_generator_mem(fib)

    print([i for i in gen1(5)])
    print([i for i in gen2(5)])
    start = time()
    print([i for i in gen3(25)])
    print(time()-start)
    start = time()
    print([i for i in gen3(25)])
    print(time()-start)


