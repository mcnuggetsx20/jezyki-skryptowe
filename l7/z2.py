from collections.abc import Iterable

#(TODO) dodac obsluge nieskonczonych sekwencji
# czyli takich co nie maja len()

def count_matching(pred, tab):
    ans = 0
    def aux(tab):
        nonlocal ans
        match tab:
            case []: return
            case [head, *tail]:
                match pred(head):
                    case True: 
                        ans += 1
                        aux(tail)

                    case False: aux(tail)
    aux(tab)
    return ans

def forall(pred, tab : Iterable):
    match tab:
        case []: return True
        case [head, *tail]:
            match pred(head):
                case False: return False
                case True: return forall(pred, tail)

def exists(pred, tab : Iterable):
    return count_matching(pred,tab) >= 1

def atleastn(n, pred, tab : Iterable):
    return count_matching(pred,tab) >= n

def atmost(n, pred, tab : Iterable):
    return count_matching(pred,tab) <= n

if __name__ == '__main__':
    print(forall(lambda x: x < 10, [1, 10,11,12]))
    print(exists(lambda x: x < 10, [1, 10,11,12]))
    print(atleastn(2, lambda x: x < 10, [1, 10,11,12]))

