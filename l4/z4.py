import sys
import csv
from collections import Counter

def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Błąd: Plik '{file_path}' nie istnieje.", file=sys.stderr)
        return
    
    char_count = len(content)
    words = content.split()
    word_count = len(words)
    lines = content.splitlines()
    line_count = len(lines)
    
    char_counter = Counter(content)
    most_common_char = char_counter.most_common(1)[0][0] if char_counter else ''
    
    word_counter = Counter(words)
    most_common_word = word_counter.most_common(1)[0][0] if word_counter else ''
    
    result = [file_path, char_count, word_count, line_count, most_common_char, most_common_word]
    
    writer = csv.writer(sys.stdout)
    writer.writerow(result)

def main():
    if len(sys.argv) < 2:
        print("Błąd: Podaj ścieżkę do pliku.", file=sys.stderr)
        return
    
    file_path = sys.argv[1]
    analyze_file(file_path)

if __name__ == "__main__":
    main()
