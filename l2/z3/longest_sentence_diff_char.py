import sys

def longest_sentence_diff_char():
    longest_sentence_length = 0
    longest_sentence = ''
    try:
        for line in sys.stdin:
            sentence = ''
            sentence_size = 0
            sentence_started = False
            last_char = ''
            can_be_longest = True
            for char in line:
                    if sentence_started:
                        if sentence[-1] == ' ':
                            if last_char.lower() == char.lower():
                                  can_be_longest = False
                            if char != ' ':
                                last_char = char
                        sentence_size += 1
                        sentence += char

                    if char == '.' or char == '!' or char == '?':
                        if sentence_started:
                            if sentence_size > longest_sentence_length and can_be_longest:
                                 longest_sentence_length = sentence_size
                                 longest_sentence = sentence
                        sentence_started = False
                        sentence = ''
                        sentence_size = 0
                        last_char = ''
                        can_be_longest = True
                    elif char.isupper() and not sentence_started:
                        sentence_started = True
                        sentence_size = 1
                        sentence += char
                        last_char = char
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    return longest_sentence

if __name__ == '__main__':
     print(longest_sentence_diff_char())