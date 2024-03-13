from input.config import Config
from utils.decorators import print_exec_time
from utils.directory_util import *
from typing import Callable
from multiprocessing import Process
from os.path import join as path_join
import os
import random


WORD_BEGIN = "آأإابتثجحخدذرزسشصضطظعغفقكلمنهوؤيئ"
WORD_MIDDLE = "ءآأإابتثجحخدذرزسشصضطظعغفقكلمنهوؤيئ"
WORD_END = "ءآأإابتثجحخدذرزسشصضطظعغفقكلمنهوؤيئىة"
DIACRITICS = "ًٌٍَُِّْ"

FORMS = {
    'ء': 1,
    'آ': 2,
    'أ': 2,
    'إ': 2,
    'ا': 2,
    'ب': 4,
    'ت': 4,
    'ث': 4,
    'ج': 4,
    'ح': 4,
    'خ': 4,
    'د': 2,
    'ذ': 2,
    'ر': 2,
    'ز': 2,
    'س': 4,
    'ش': 4,
    'ص': 4,
    'ض': 4,
    'ط': 4,
    'ظ': 4,
    'ع': 4,
    'غ': 4,
    'ف': 4,
    'ق': 4,
    'ك': 4,
    'ل': 4,
    'م': 4,
    'ن': 4,
    'ه': 4,
    'و': 2,
    'ؤ': 2,
    'ي': 4,
    'ئ': 4,
    'ى': 3,
    'ة': 2,
}


def generate_diacritics() -> str:
    return random.choice(DIACRITICS)


def get_alpha_set() -> list:
    return sorted(list(set(WORD_BEGIN+WORD_MIDDLE+WORD_END)))


def generate_words_with_diacritics(word: str) -> str:
    return ''.join(f'{l}{generate_diacritics()}' for l in word)


def generate_words_without_diacritics(word: str) -> str:
    return ''.join(f'{l}' for l in word)


def generate_letters(path: str) -> None:
    ALPHA_SET = get_alpha_set()
    with open(path, 'w+', encoding='utf8') as words_container:
        lines = []
        for c in ALPHA_SET:
            lines.append(c)
            for f in range(1, FORMS[c]+1):
                for d in DIACRITICS:
                    final = ''
                    match f:
                        case 1:
                            final = [f"{c}", f"{c}{d}"][Config.IS_WITH_DIACRITICS]
                        case 2:
                            final = [f"ـ{c}", f"ـ{c}{d}"][Config.IS_WITH_DIACRITICS]
                        case 3:
                            final = [f"{c}ـ", f"{c}{d}ـ"][Config.IS_WITH_DIACRITICS]
                        case 4:
                            final = [f"ـ{c}ـ", f"ـ{c}{d}ـ"][Config.IS_WITH_DIACRITICS]
                    lines.append(final)
        lines = sorted(list(set(lines)))
        words_container.write('\n'.join(lines)+'\n')


def generate_two_char_words(path: str, collections: tuple[str, str, str], generator: Callable) -> None:
    BEGIN = collections[0]
    MIDDLE = collections[1]
    END = collections[2]
    with open(path, 'w+', encoding='utf8') as words_container:
        for i in BEGIN:
            for j in END:
                result = generator(i + j)
                words_container.write(result + "\n")


def generate_three_char_words(path: str, collections: tuple[str, str, str], generator: Callable) -> None:
    BEGIN = collections[0]
    MIDDLE = collections[1]
    END = collections[2]
    with open(path, 'w+', encoding='utf8') as words_container:
        for i in BEGIN:
            for j in MIDDLE:
                for k in END:
                    result = generator(i + j + k)
                    words_container.write(result + "\n")


def generate_four_char_words(path: str, collections: tuple[str, str, str], generator: Callable) -> None:
    BEGIN = collections[0]
    MIDDLE = collections[1]
    END = collections[2]
    with open(path, 'w+', encoding='utf8') as words_container:
        for i in BEGIN:
            for j in MIDDLE:
                for k in MIDDLE:
                    for l in END:
                        result = generator(i + j + k + l)
                        words_container.write(result + "\n")


def generate_five_char_words(path: str, collections: tuple[str, str, str], generator: Callable) -> None:
    BEGIN = collections[0]
    MIDDLE = collections[1]
    END = collections[2]
    with open(path, 'w+', encoding='utf8') as words_container:
        for i in BEGIN:
            for j in MIDDLE:
                for k in MIDDLE:
                    for l in MIDDLE:
                        for m in END:
                            result = generator(i + j + k + l + m)
                            words_container.write(result + "\n")


def generate_six_char_words(path: str, collections: tuple[str, str, str], generator: Callable) -> None:
    BEGIN = collections[0]
    MIDDLE = collections[1]
    END = collections[2]
    with open(path, 'w+', encoding='utf8') as words_container:
        for i in BEGIN:
            for j in MIDDLE:
                for k in MIDDLE:
                    for l in MIDDLE:
                        for m in MIDDLE:
                            for n in END:
                                result = generator(i + j + k + l + m + n)
                                words_container.write(result + "\n")


def generate_words(length: int, path: str, collections: tuple[str, str, str], generator: Callable[[str], str]):
    [
        generate_two_char_words,
        generate_three_char_words,
        generate_four_char_words,
        generate_five_char_words,
        generate_six_char_words,
    ][length-2](path, collections, generator)


def calc_gen_words(word_length: int) -> int:
    if word_length == 1:
        return sum([FORMS[c]*len(DIACRITICS)+1 for c in get_alpha_set()])
    return len(WORD_BEGIN) * len(WORD_MIDDLE)**(word_length-2) * len(WORD_END)


def calc_expected_size(min: int, max: int, with_diacritics: bool = True) -> int:
    total_size = 0
    for length in range(min, max+1):
        words_count = calc_gen_words(length)
        newline_size = words_count * len('\r\n'.encode('utf8'))
        words_size = words_count * length * len('ض'.encode('utf8')) * (int(with_diacritics)+1)
        total_size += newline_size + words_size
    return total_size


def calc_gen_words_in_range(min: int, max: int) -> int:
    return sum(calc_gen_words(len) for len in range(min, max+1))


def calc_gen_letter(letter: str, length: int) -> int:
    alpha = get_alpha_set()
    alpha_len = len(alpha)
    occur = WORD_BEGIN.count(letter) + WORD_MIDDLE.count(letter)*(length-2) + WORD_END.count(letter)
    return occur*alpha_len**(length-1)


def calc_gen_letter_in_range(letter: str, min_length: int, max_length: int) -> int:
    alpha = get_alpha_set()
    alpha_len = len(alpha)
    begin = WORD_BEGIN.count(letter)
    middle = WORD_MIDDLE.count(letter)
    end = WORD_END.count(letter)
    total = [0, FORMS[letter]*len(DIACRITICS)+1][min_length == 1]
    for length in range(min(min_length, 2), max_length+1):
        occur = begin + middle*(length-2) + end
        total += occur*alpha_len**(length-1)
    return total


def generate(length: int):
    words_generator = [
        generate_words_without_diacritics,
        generate_words_with_diacritics
    ][Config.IS_WITH_DIACRITICS]
    processes: list[Process] = [
        [
            Process(
                target=generate_words,
                args=(
                    length,
                    path_join(Config.OUTPUT_WORDS_PATH, f'words-{length}-{i}.txt'),
                    (WORD_BEGIN[i], WORD_MIDDLE, WORD_END),
                    words_generator,
                )
            )
            for i in range(len(WORD_BEGIN))
        ],
        [
            Process(
                target=generate_letters,
                args=(
                    path_join(Config.OUTPUT_WORDS_PATH, f'words-{length}.txt'),
                )
            )
        ],
    ][length == 1]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    if length == 1:
        return

    total_path = path_join(Config.OUTPUT_WORDS_PATH, f'words-{length}.txt')
    output_paths = [
        path_join(Config.OUTPUT_WORDS_PATH, f'words-{length}-{i}.txt')
        for i in range(len(WORD_BEGIN))
    ]
    DirectoryUtil.merge_files(output_paths, total_path)
    for path in output_paths:
        os.remove(path)


def convert_to_suitable_size(size_in_bytes: int) -> str:
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    size = size_in_bytes
    while size >= 1024 and unit_index < len(units):
        size /= 1024
        unit_index += 1
    return f'{size: 0.02f} {units[unit_index]}'


class GenerateRandomWords(object):
    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    @print_exec_time
    def generate(self) -> None:
        MIN_LENGTH = self.min
        MAX_LENGTH = self.max
        format = ','

        counts = []
        for l in range(MIN_LENGTH, MAX_LENGTH+1):
            counts.append(calc_gen_words(l))
            print(f"Words with {l} letters: {counts[-1]: {format}}")

        words_count = sum(counts)
        letters_count = sum(counts[i-MIN_LENGTH]*i for i in range(MIN_LENGTH, MAX_LENGTH+1))
        size = convert_to_suitable_size(calc_expected_size(MIN_LENGTH, MAX_LENGTH))
        print()
        print(f"Words in total: {words_count: {format}}")
        print(f"Letters in total: {letters_count: {format}}")
        print(f"Expected size: {size}")
        print()
        print(f"Occurrences of letters: ")

        alpha = get_alpha_set()
        letter_per_line = 5
        for i in range(0, len(alpha), letter_per_line):
            counts = [f"{c}: {calc_gen_letter_in_range(c, MIN_LENGTH, MAX_LENGTH)}" for c in alpha[i:min(i+letter_per_line, len(alpha))]]
            print('\t'+',\t'.join(counts))
        GenerateRandomWords._main(MIN_LENGTH, MAX_LENGTH)
        print()

    @staticmethod
    def _main(min, max):
        processes: list[Process] = [Process(target=generate, args=(length,)) for length in range(min, max+1)]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        with open(Config.OUTPUT_WORDS_RANDOM_FILE, 'w+', encoding='utf8') as base_words_file:
            for length in range(min, max+1):
                path = path_join(Config.OUTPUT_WORDS_PATH, f'words-{length}.txt')
                with open(path, 'r', encoding='utf8') as words_file:
                    base_words_file.write(words_file.read()+'\n')
                os.remove(path)


if __name__ == "__main__":
    generator = GenerateRandomWords(1, 3)
    generator.generate()
