import argparse
from datetime import datetime
from random import choice
from numpy import mean, std
import lib
import logging
import sys

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)

stdout = logging.StreamHandler(sys.stdout)
stdout.setLevel(logging.DEBUG)
stdout.addFilter(lambda record: record.levelno < logging.ERROR)
stdout.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(stdout)

stderr = logging.StreamHandler(sys.stderr)
stderr.setLevel(logging.ERROR)
stderr.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(stderr)

######  ARGPARSE
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--quantity', type=str, required = True,help='Quantity to measure')
parser.add_argument('--frequency', type=str, required=True,help='Frequency of the measurement')
parser.add_argument('--begin', type=str, required=True,help='Begin date')
parser.add_argument('--end', type=str, required=True,help='End date')

subparsers = parser.add_subparsers(dest='command', required=True)

show_random_parser = subparsers.add_parser('show_random', help='kdfj')
calc_parser = subparsers.add_parser('calc', help='')
calc_parser.add_argument('--station', type=str, required=True, help='Which station to calculate for')

args = parser.parse_args()
#######

files = lib.get_measurements(args.quantity, args.frequency)
if not files: 
    logging.warning(f'Could not find files with specified parameters')

filedata_dicts = list()
for file in files:
    ### czytanie pliku
    filedata = []
    with open(file, 'r') as csv:

        logger.info(f'Opened file: {file}.') ## log

        for line in csv:
            filedata.append(line.split(','))
            logger.debug(f'Read {len(line)} bytes of data.') ## log

    logger.info(f'Closed file: {file}.') ## log
    #####

    ### parsowanie do dicta
    headers = [i[0] for i in filedata]
    temp = []

    for i, v in enumerate(filedata[0]):
        column = [line[i] for line in filedata]
        temp.append(dict(zip(headers, column)))
    filedata_dicts.append(temp[1:])
    #####

def parse_data(func):

    try:
        dates = (
                datetime.strptime(args.begin, "%Y-%m-%d"), 
                datetime.strptime(args.end, '%Y-%m-%d')
        )
    except ValueError as e:
        logger.critical('Invalid dates.')
        exit(1)

    if dates[0] > dates[1]:
        logger.error('"begin date" can not be bigger than "end date"')

    for filedata_dict in filedata_dicts:
        for i in filedata_dict[1:]:
            for key in i.keys():
                try: 
                    date = datetime.strptime(key, '%m/%d/%y %H:%M')
                    if date >= dates[0] and date <= dates[1]:
                        func(i, key)
                        break

                except ValueError: continue

if __name__ == '__main__':

    if args.command == 'show_random':
        st = set()
        parse_data(lambda line,_ : st.add(line['Kod stacji']))
        if not st: 
            st.add('')
            logger.warning('Could not find measurements for given parameters')

        print(choice(list(st)))
    
    elif args.command == 'calc':

        # na przyklad: python z5.py --quantity PM10 --frequency 24g --begin 2023-01-01 --end 2023-04-20 calc --station LdOpocSkCuri
        numbers = list()
        def solve(line, key):
            if args.station == line['Kod stacji']:
                numbers.append(float(line[key]))
            return

        parse_data(solve)
        if numbers:
            print(f'Dane dla {args.station}, {args.quantity}:')
            print(f'Srednia: {mean(numbers)}\nOdchylenie: {std(numbers)}')
        else:
            logger.warning('Could not find measurements for given parameters')




