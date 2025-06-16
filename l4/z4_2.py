import subprocess
import os
import csv
from collections import Counter
import sys
import json

def run_analysis_on_file(filepath):
    result = subprocess.run(
        ["python3", "z4.py", "--with_counters"],
        input=f"{filepath}\n",
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None

    reader = csv.reader(result.stdout.strip().split('\n'))
    row = next(reader)
    return {
        "path": row[0],
        "chars": int(row[1]),
        "words": int(row[2]),
        "lines": int(row[3]),
        "most_common_chars_counter": json.loads(row[4]),
        "most_common_words_counter": json.loads(row[5]),
    }

def main(directory):
    # Analizing every file in directory
    results = []
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if os.path.isfile(full_path):
            result = run_analysis_on_file(full_path)
            if result:
                results.append(result)
    
    if not results:
        print("Brak wyników.")
        return
    # Standard adding
    total_files = len(results)
    total_chars = sum(r["chars"] for r in results)
    total_words = sum(r["words"] for r in results)
    total_lines = sum(r["lines"] for r in results)
    # Adding from different files counters so it will return most commons from across files
    all_chars = Counter()
    all_words = Counter()
    for r in results:
        all_chars.update(r["most_common_chars_counter"]) 
        all_words.update(r["most_common_words_counter"])
    most_common_char = all_chars.most_common(1)[0][0]
    most_common_word = all_words.most_common(1)[0][0]
    # Printing every data
    print("LICZBA_PLIKÓW:", total_files)
    print("SUMA_ZNAKÓW:", total_chars)
    print("SUMA_SŁÓW:", total_words)
    print("SUMA_WIERSZY:", total_lines)
    print("NAJCZĘSTSZY_ZNAK:", most_common_char)
    print("NAJCZĘSTSZE_SŁOWO:", most_common_word)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception ('Directory not given')
    else:
        main(sys.argv[1])
