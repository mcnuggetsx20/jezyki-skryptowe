import sys

def percentage_sentences_with_proper_names():
    longest_sentence_length = 0
    longest_sentence = ''
    try:
        for line in sys.stdin:
            sentence = ''
            sentence_size = 0
            sentence_started = False
            for char in line:
                    if sentence_started:
                        sentence_size += 1
                        sentence += char

                    if char == '.' or char == '!' or char == '?':
                        if sentence_started:
                            if sentence_size > longest_sentence_length:
                                 longest_sentence_length = sentence_size
                                 longest_sentence = sentence
                        sentence_started = False
                        sentence = ''
                        sentence_size = 0
                    elif char.isupper() and not sentence_started:
                        sentence_started = True
                        sentence_size = 1
                        sentence += char
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    return longest_sentence

if __name__ == '__main__':
     print(percentage_sentences_with_proper_names())