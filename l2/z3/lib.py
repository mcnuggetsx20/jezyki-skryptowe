from sys import stdin

def filter(check_function) -> str:
    sentence = ''
    result = ''
    for line in stdin:
        sentence = ''
        for i,v in enumerate(line):
            if v == '.' or v == '!' or v == '?' or v == '…' or v=='\n':

                if len(sentence) == 0:
                    sentence = ''
                    continue

                if i+1 < len(line):
                    if line[i+1] == '!' or line[i+1] == '?':
                        sentence += v
                        continue

                ### wykrywanie dialogu
                temp_sentence = sentence.strip()
                hyphen = 2 if temp_sentence[:2] == '— ' else 0
                temp_sentence = temp_sentence[hyphen::]
                temp_sentence += v
                ###

                ### uznajemy ze fraza z jednym slowem nie moze byc zdaniem
                # print( [temp_sentence], hyphen)
                word_count = temp_sentence.count(' ') + 1
                if word_count >= 2:
                    result += f'{temp_sentence}\n' * check_function(temp_sentence)

                sentence = ''

            else:
                sentence += v

    return result

