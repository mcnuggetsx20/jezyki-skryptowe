import sys
import time

# Reading head of the file
def read_head(file, num_lines=10):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for _ in range(num_lines):
                line = f.readline()
                if not line:
                    break
                print(line, end='')
    except Exception as e:
        raise e

# Reading head of stdin
def read_head_stdin(num_lines=10):
    for _ in range(num_lines):
        line = sys.stdin.readline()
        if not line:
            break
        print(line, end='')

# Folowing file
def follow(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if line:
                    print(line, end='')
                else:
                    time.sleep(1)
    except Exception as e:
        raise e

def main():
    args = sys.argv[1:]
    num_lines = 10
    follow_mode = False
    file_path = None
    if (len(args)>3):
        raise Exception("Zbyt wiele argumentow")
    
    for arg in args:
        if arg.startswith('--lines='):
            try:
                num_lines = int(arg.split('=')[1])
            except Exception as e:
                raise Exception("Liczba nie jest intem w --lines")
        elif arg == '--follow':
            follow_mode = True
        else:
            file_path = arg
    
    if file_path:
        if follow_mode:
            follow(file_path)
        else:
            read_head(file_path, num_lines)
    else:
        read_head_stdin(num_lines)

if __name__ == "__main__":
    main()
