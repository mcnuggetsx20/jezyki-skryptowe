import sys

def first_sentence_with_subordinate_clauses(min_number_of_commas=3):
    try:
        for line in sys.stdin:
            sentence = ''
            sentence_started = False
            number_of_commas = 0
            for char in line:
                    if sentence_started:
                        if char == ',':
                            number_of_commas +=1
                        sentence += char

                    if char == '.' or char == '!' or char == '?':
                        if sentence_started:
                            if number_of_commas>=min_number_of_commas:
                                return sentence
                        sentence_started = False
                        sentence = ''
                        number_of_commas = 0
                    elif char.isupper() and not sentence_started:
                        sentence_started = True
                        sentence += char
    except Exception as e:
        print(f"Błąd podczas przetwarzania wejścia: {e}")
    return ''

if __name__ == '__main__':
     print(first_sentence_with_subordinate_clauses())