from collections.abc import Iterable

def count_matching(pred, tab, lo=0, hi=0, check_all=False):
    if not hasattr(tab, '__len__'):
        raise Exception('Invalid Input')

    ans = 0
    def aux(tab):
        nonlocal ans,lo, hi
        if lo and lo == ans: return
        if hi and hi < ans: return

        match tab:
            case []: return
            case [head, *tail]:

                res = pred(head)
                if not res and check_all:
                    return 

                ans += res
                aux(tail)
    aux(tab)
    if check_all:
        return ans ==len(tab)

    if lo and hi: return lo <= ans <= hi
    elif lo: return lo <= ans
    elif hi: return ans <= hi
    elif check_all: return ans == len(tab)
    else: return ans

def forall(pred, tab : Iterable):
    return count_matching(pred, tab, check_all=True)

def exists(pred, tab : Iterable):
    return count_matching(pred,tab, lo=1)

def atleastn(n, pred, tab : Iterable):
    return count_matching(pred,tab,lo=n)

def atmost(n, pred, tab : Iterable):
    return count_matching(pred,tab,hi=n)

if __name__ == '__main__':
    print(forall(lambda x: x < 10, [1, 10,11,12]))
    print(exists(lambda x: x < 10, [1, 10,11,12]))
    print(atleastn(2, lambda x: x < 10, [1, 10,11,12]))
    print(atmost(2, lambda x: x < 10, [1, 10,11,12]))
    print(forall(lambda x: x < 10, range(0,100)))

