import sys

def count_non_whitespace_chars() -> int:
    count = 0
    try:
        while True:
            char = sys.stdin.read(1)
            if not char:
                break
            if not_white_char(char):
                count+=1
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    return count

def not_white_char(char):
    if char!=' ' and char!='\n' and char!='\t':
        return True
    return False

if __name__ == '__main__':
    print(count_non_whitespace_chars())