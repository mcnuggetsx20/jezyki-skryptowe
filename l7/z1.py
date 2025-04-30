from collections.abc import Sequence


#(TODO) potencjalnie trzeba zmienic to odwracanie tekstu
def odwr(text : str):
    match text:
        case '': return ''
        case _: return text[-1] + odwr(text[:-1])

def most_common_element(tab : list):
    def aux(tab: list, dc : dict):
        match tab:
            case []: return dc
            case [head, *tail]:
                dc[head] += 1
                return aux(tail, dc)
    dc = {i : 0 for i in tab}
    aux(tab, dc)

    # dc = {i : tab.count(i) for i in tab}
    return sorted([(dc[k], k) for k in dc])[-1][1]

def newt(x, epsilon):
    match x >= 0:
        case True: pass
        case False: raise Exception("Niewlasciwa liczba")

    def aux(y):
        match abs(y**2 - x) < epsilon:
            case True: return y
            case _:
                return(aux(0.5 * (y+ x/y)))
    return aux(x)

def make_alpha_dict(text):
    words = text.split()
    dc = {i : [] for i in text if i != ' '}
    
    def aux(part):
        match list(part):
            case []: return
            case [head, *tail]:
                match head:
                    case ' ': return aux(tail)
                    case _:
                        dc[head] = [word for word in words if head in word]
                        aux(tail)
                        return
    
    aux(text)
    return dc

def flatten(x):
    match isinstance(x, Sequence):
        case False: return [x]
        case True:
            match list(x):
                case []: return []
                case [head, *tail]:
                    return flatten(head) + flatten(tail)


if __name__ == '__main__':
    print(most_common_element([2,2,10]))
    print(newt(49, 0.1))
    print(make_alpha_dict('ona i on'))
    print(flatten([1, [2, 3], [[4, 5], 6]]))
