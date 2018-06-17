# Sam As End

import csv
import math


def is_in_ethiopian_unicode_block(character: str) -> bool:
    return ord('ሀ') <= ord(character) <= ord('፼')


def are_all_in_ethiopian_unicode_block(characters: str) -> bool:
    for character in characters:
        if not is_in_ethiopian_unicode_block(character):
            return False
    return True if len(characters) > 0 else False


def increment_value(dictionary: dict, key: str) -> None:
    try:
        dictionary[key] += 1
    except KeyError:
        dictionary[key] = 1


def bet(character: str) -> str:
    class NotAnEthiopicCharacterException(TypeError):
        pass

    if not is_in_ethiopian_unicode_block(character):
        raise NotAnEthiopicCharacterException()

    # Every row consisted of two 'bet's taking half of nibble each.
    # We can observe that every 'start of a 'bet'' last
    # nibble is 0 (0b0000) or 8 (0b1000), It's obvious that
    # last 3 bit are the one who determine the variant
    return chr(ord(character) >> 3 << 3)


def col(character: str) -> str:
    class NotAnEthiopicCharacterException(TypeError):
        pass

    if not is_in_ethiopian_unicode_block(character):
        raise NotAnEthiopicCharacterException()

    return chr(ord('1') + (ord(character) & 0x7))


def main():
    # various letter based frequencies
    letter, bigraph, trigraph = ({}, {}, {})

    bet_graph, col_graph, double_letter = ({}, {}, {})

    # various word based frequencies
    first_letter, second_letter = ({}, {})
    word_length, last_letter = ({}, {})

    # cache the last two letters
    penultimate = last = '\u0000'

    # cache for word based analysis
    word = ''
    line_no = 0

    with open('combined.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            line_no += 1

            print('Line:  %6d Percentage: %3d%%' % (line_no, math.floor((line_no * 100) / 2245892)))

            for character in line:
                if is_in_ethiopian_unicode_block(character):
                    increment_value(letter, character)
                    increment_value(bet_graph, bet(character))
                    increment_value(col_graph, col(character))

                    increment_value(first_letter, character) if last.isspace() else 0
                    increment_value(second_letter, character) \
                        if is_in_ethiopian_unicode_block(last) and penultimate.isspace() else 0

                    if is_in_ethiopian_unicode_block(last):
                        increment_value(bigraph, last + character)

                        if is_in_ethiopian_unicode_block(penultimate):
                            increment_value(trigraph, penultimate + last + character)

                    increment_value(double_letter, character) if character == last else 0
                elif character.isspace():
                    increment_value(last_letter, last) if is_in_ethiopian_unicode_block(last) else 0

                    word = word.strip().strip(
                        ''.join([chr(other_ethiopic) for other_ethiopic in range(ord('ፖ') + 1, ord('፼'))]))

                    if are_all_in_ethiopian_unicode_block(word):
                        increment_value(word_length, str(len(word)))

                    word = ''

                penultimate = last
                last = character
                word += character

        frequencies = dict(
            letter=letter, bigraph=bigraph, trigraph=trigraph, double_letter=double_letter,
            first_letter=first_letter, second_letter=second_letter, bet_graph=bet_graph,
            last_letter=last_letter, col_graph=col_graph, word_length=word_length)

        for frequency in frequencies:
            stats = [{'Character': '' + k, 'Count': frequencies[frequency][k]} for k in frequencies[frequency].keys()]
            with open('../csv/' + frequency + '.csv', 'w') as csv_file:
                w = csv.DictWriter(csv_file, ['Character', 'Count'])
                w.writeheader()
                w.writerows(sorted(stats, key=lambda stat: stat['Count'], reverse=True))


if __name__ == '__main__':
    main()
    print('Done analyzing the frequency')
