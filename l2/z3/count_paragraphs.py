import sys

def count_paragraphs() -> int:
    line_with_chars = False
    empty_line = False
    count = 0
    try:
        for line in sys.stdin:
            if all_white_chars(line):
                empty_line = True
                if line_with_chars and empty_line:
                    count+=1
                line_with_chars = False
            else:
                line_with_chars = True
                empty_line = False
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    if line_with_chars:
        return count+1
    else:
        return count

def all_white_chars(line):
    for char in line:
        if char!=' ' and char!='\n' and char!='\t':
            return False
    return True

if __name__ == '__main__':
    print(count_paragraphs())