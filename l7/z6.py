from time import time
from logging import getLogger,StreamHandler, DEBUG
from sys import stdout

def log(log_level):
    def make_decorator(obj):
        logger = getLogger("wrapper_logger")
        logger.setLevel(DEBUG)
        if not logger.handlers: logger.addHandler(StreamHandler(stdout))
        log_dict = dict()

        if isinstance(obj, type):
            old_init = obj.__init__
            def new_init(self, *args, **kwargs):
                old_init(self, *args, **kwargs)
                logger.log(log_level, f"Zainicjowano instancje klasy {obj.__name__}")
                return
            
            obj.__init__ = new_init
            return obj

        elif callable(obj):

            def wrapper(*args, **kwargs):

                start_time = time()
                log_dict[start_time] = 'Czas wywołania: '

                result = obj(*args, **kwargs)

                log_dict[time() - start_time] = 'Czas trwania: '
                log_dict[result] = f'Wartość zwracana: {obj.__name__}({args}, {kwargs}) -> '

                for value,info in log_dict.items():
                    logger.log(log_level, f'{info}{value}')

                return result

            return wrapper

    return make_decorator

@log(DEBUG)
def foo(n):
    return n * 2

@log(DEBUG)
class Test:
    def __init__(self):
        return

if __name__ == '__main__':
    Test()
    foo(2)
    pass

