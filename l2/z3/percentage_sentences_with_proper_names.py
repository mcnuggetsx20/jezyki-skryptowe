import sys

def percentage_sentences_with_proper_names():
    sentences = 0
    sentences_with_proper_names = 0
    try:
        for line in sys.stdin:
            sentence_started = False
            sentence_has_proper_name = False
            for char in line:
                    if char.isupper() and sentence_started:
                        sentence_has_proper_name = True

                    if char == '.' or char == '!' or char == '?':
                        if sentence_started:
                            sentences += 1
                            if sentence_has_proper_name:
                                sentences_with_proper_names += 1
                        sentence_started = False
                        sentence_has_proper_name = False
                    elif char.isupper() and not sentence_started:
                        sentence_started = True
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    if sentences == 0:
        raise Exception("Brak zdan w tekscie")  
    return sentences_with_proper_names/sentences *100.0

if __name__ == '__main__':
    try:
        print(percentage_sentences_with_proper_names())
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")