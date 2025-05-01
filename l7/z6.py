from time import time
from logging import getLogger,StreamHandler, DEBUG
from sys import stdout

def log(log_level):
    def make_decorator(obj):
        logger = getLogger("wrapper_logger")
        logger.setLevel(DEBUG)
        logger.addHandler(StreamHandler(stdout))
        log_dict = dict()

        
        if isinstance(obj, type):
            old_init = obj.__init__
            print('aa')
            def new_init(self, *args, **kwargs):
                print('elo')
                # logger.log(log_level, "Zainicjowano instancje klasy")
                old_init(self, *args, **kwargs)
                return
            
            obj.__init__ = new_init
            return obj

        elif callable(obj):

            def wrapper(*args, **kwargs):

                start_time = time()
                log_dict[start_time] = 'Czas wywołania: '

                result = obj(*args, **kwargs)

                log_dict[time() - start_time] = 'Czas trwania: '
                log_dict[result] = 'Wartość zwracana: '

                for value,info in log_dict.items():
                    logger.log(log_level, f'{info}{value}')

                return result

            return wrapper

    return make_decorator

@log(DEBUG)
def elo():
    return 15

@log(DEBUG)
class Test:
    def __init__(self):
        print('Tworze sie')
        return

if __name__ == '__main__':
    t = Test()

