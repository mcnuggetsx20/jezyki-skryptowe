import sys
import time

def read_head(file, num_lines=10):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for _ in range(num_lines):
                line = f.readline()
                if not line:
                    break
                print(line, end='')
    except FileNotFoundError:
        print(f"Błąd: Plik '{file}' nie istnieje.", file=sys.stderr)

def read_head_stdin(num_lines=10):
    for _ in range(num_lines):
        line = sys.stdin.readline()
        if not line:
            break
        print(line, end='')

def follow(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    print(line, end='')
                else:
                    time.sleep(1)
    except FileNotFoundError:
        print(f"Błąd: Plik '{file}' nie istnieje.", file=sys.stderr)

def main():
    args = sys.argv[1:]
    num_lines = 10
    follow_mode = False
    file_path = None
    
    for arg in args:
        if arg.startswith('--lines='):
            try:
                num_lines = int(arg.split('=')[1])
            except ValueError:
                print("Błąd: Niepoprawna liczba w '--lines=n'", file=sys.stderr)
                return
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
