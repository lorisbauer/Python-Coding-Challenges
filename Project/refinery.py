def converter(text: str) -> list:
    tokenized = sent_tokenize(text)
    solutions = []
    solution = ''

    for sentence in tokenized:
        for _, letter in enumerate(sentence):
            if letter in list(change.keys()):
                letter = change.get(letter)
            solution += letter
        solutions.append(solution)
        solution = ''
    return solutions


def read_file(file, encoder='utf-8') -> str:
    text = ''
    with open(file, 'r', encoding=encoder) as f:
        for line in f:
            line = line.strip()
            text += str(line)
            text += ' '
    return text


def clean_sent(elements: list):
    for i, word in enumerate(elements):
        if '.' in word and len(word) > 1 and word.count('.') == 1:
            splitted = word.split('.')
            splitted.insert(1, '.')
            if not splitted[-1]:
                splitted.pop(-1)
            elif len(splitted) > 2 and splitted[-1][0].islower():
                splitted[-1] = splitted[-1].capitalize()
            elements.pop(i)
            for j, elem in enumerate(splitted):
                elements.insert(i + j, elem)
    return elements


def write_file(f, elements: str) -> None:
    for element in sent_tokenize(elements):
        words = clean_sent(word_tokenize(element))
        line = ''
        line_length = 0
        for i, word in enumerate(words):
            if i + 1 < len(words):
                if words[i + 1].strip() not in general and words[i].strip() not in exceptions:
                    word = word.strip() + ' '
            if line_length + len(word) <= max_length or word.strip() in punctuation:
                if word.strip() in punctuation:
                    word = word.strip() + ' '
                line += word
                line_length += len(word)
            else:
                f.write(line)
                f.write('\n')
                line_length = 0
                line = word
        if line:
            f.write(line)
        f.write('\n')


def translate(text: list) -> None:
    if not text:
        raise ValueError
    start = perf_counter()

    with open('result.txt', 'w', encoding='utf-8') as f:
        element = ''.join(text)
        if translator.get_usage().character.count + len(element) < translator.get_usage().character.limit:
            element = translator.translate_text(element, source_lang=source_lang, target_lang=target_lang).text
        else:
            print(f'Limit exceeded, Current usage: {translator.get_usage().character.count}')
        write_file(f, element)

    print(f'\nCurrent usage: {translator.get_usage().character.count}, '
          f'Remaining: {translator.get_usage().character.limit - translator.get_usage().character.count}')
    print(f'Translation Time: {perf_counter() - start}s')


if __name__ == '__main__':
    from deepl import Translator
    from os import startfile
    from nltk.tokenize import sent_tokenize, word_tokenize
    from string import punctuation
    from time import perf_counter

    translator = Translator('748eb8fd-6a1f-6bb9-aef4-33a367936efb:fx')
    content = read_file('sample.txt')

    source_lang = 'FR'
    target_lang = 'DE'

    quotation = "'"
    max_length = 100
    general = [*punctuation, quotation, '’']
    exceptions = ['(', '’', '``']
    change = {
        'Ù': 'ô',
        'Á': 'ç',
        'È': 'é', 'Ë': 'è',
        '˘': 'ù', '˚': 'û',
        'Ó': 'î', 'Í': 'î', 'Ô': 'ï',
        '‡': 'à', '°': 'à', '¿': 'À', '‚': 'â',
        '"': quotation, '»': quotation
    }
    converted = converter(content)
    translate(converted)
    startfile('result.txt')
