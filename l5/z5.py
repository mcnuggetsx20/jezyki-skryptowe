import argparse
from datetime import datetime
from random import choice
import lib

######  ARGPARSE
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--quantity', type=str, required = True,help='Quantity to measure')
parser.add_argument('--frequency', type=str, required=True,help='Frequency of the measurement')
parser.add_argument('--begin', type=str, required=True,help='Begin date')
parser.add_argument('--end', type=str, required=True,help='End date')

subparsers = parser.add_subparsers(dest='command', required=True)

show_random_parser = subparsers.add_parser('show_random', help='kdfj')
calc_parser = subparsers.add_parser('calc', help='')

args = parser.parse_args()
#######

files = lib.get_measurements(args.quantity, args.frequency)
filedata_dicts = list()
for file in files:
    ### czytanie pliku
    filedata = []
    with open(file, 'r') as csv:
        for line in csv:
            filedata.append(line.split(','))
    ########

    ### parsowanie do dicta
    headers = [i[0] for i in filedata]
    temp = []

    for i, v in enumerate(filedata[0]):
        column = [line[i] for line in filedata]
        temp.append(dict(zip(headers, column)))
    filedata_dicts.append(temp[1:])
    #####

st = set()
dates = (
        datetime.strptime(args.begin, "%Y-%m-%d"), 
        datetime.strptime(args.end, '%Y-%m-%d')
)

if __name__ == '__main__':

    if args.command == 'show_random':
        for filedata_dict in filedata_dicts:
            for i in filedata_dict[1:]:
                for key in i.keys():
                    try: 
                        date = datetime.strptime(key, '%m/%d/%y %H:%M')
                        if date >= dates[0] and date <= dates[1]:
                            st.add(i['Kod stacji'])
                            break

                    except ValueError: continue

        print(choice(list(st)))

    elif args.command == 'calc':
        for filedata_dict in filedata_dicts:
            for i in filedata_dict[1:]:
                for key in i.keys():
                    try: 
                        date = datetime.strptime(key, '%m/%d/%y %H:%M')
                        if date >= dates[0] and date <= dates[1]:
                            st.add(i['Kod stacji'])
                            break

                    except ValueError: continue



