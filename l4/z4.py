import sys
import csv
from collections import Counter
import json

def analyze_file(file_path, with_counter=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise Exception("File not found")
    
    char_count = len(content)
    words = content.split()
    word_count = len(words)
    lines = content.splitlines()
    line_count = len(lines)

    # Using counter for counting most commons
    char_counter = Counter(content)
    most_common_char = char_counter.most_common(1)[0][0] if char_counter else ''
    
    word_counter = Counter(words)
    most_common_word = word_counter.most_common(1)[0][0] if word_counter else ''
    
    # Writing output
    if with_counter:
        result = [file_path, char_count, word_count, line_count, json.dumps(char_counter),json.dumps(word_counter)]
    else:
        result = [file_path, char_count, word_count, line_count, most_common_char, most_common_word]
    
    writer = csv.writer(sys.stdout)
    writer.writerow(result)


if __name__ == "__main__":
    file_path = sys.stdin.readline().strip()
    if not file_path or file_path=='':
        raise Exception("No file_path given")
    # Added flag for 4.2
    if len(sys.argv) ==2 and sys.argv[1] == '--with_counters':
        analyze_file(file_path, True)
    else:
        analyze_file(file_path)
