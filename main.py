from input.config import *
from utils.directory_util import DirectoryUtil
from utils.decorators import print_exec_time
from utils.debug_util import Debugger
from utils.progress_util import ProgressUtil
from generators.dataset_generator import DatasetGenerator, ImageSize
from generators.words_generator import GenerateRandomWords
from scraper.web_scraper import WebScraper
from os import get_terminal_size
from os.path import exists
import subprocess
import json


def print_separator(sep: str):
    width, height = get_terminal_size()
    print('\n'+sep*width+'\n')


def answer_input(text: str) -> bool:
    return input(text).lower() in ['y', 'yes']


def count_generated_command(cmd) -> dict[str, int]:
    if Config.IS_DEBUGGING:
        print(' '.join(cmd))
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as popen:
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
    with open(Config.OUTPUT_LETTERS_COUNT_FILE, 'r', encoding='utf-8-sig') as file:
        counter: dict[str, int] = json.load(file)
    return counter


def count_generated():
    try:
        print('Count of TotalWords.txt:\n')
        counter = count_generated_command([Config.COUNTER_PROGRAM, Config.OUTPUT_WORDS_TOTAL_FILE])
    except subprocess.CalledProcessError:
        print('[x] Install .net 8.0 to get the counter!')
        pass
    alpha = sorted(list(counter.keys()))
    largest_size = len(str(max(counter.keys())))
    letter_per_line = 5
    for i in range(0, len(alpha), letter_per_line):
        counts = [f"{c}: {counter[alpha[i]]: {largest_size}}" for c in alpha[i:min(i+letter_per_line, len(alpha))]]
        print('  '+',\t'.join(counts))
    print()


def generate_words():
    paths = []
    is_missing = not (exists(Config.OUTPUT_WORDS_WEB_FILE) and exists(Config.OUTPUT_WORDS_RANDOM_FILE))
    is_random_words_included = Config.DATASET_SOURCE in [DatasetSourceEnum.Both, DatasetSourceEnum.RandomWordsOnly]
    is_web_words_included = Config.DATASET_SOURCE in [DatasetSourceEnum.Both, DatasetSourceEnum.WebWordsOnly]

    if is_missing or answer_input('Do you want to regenerate words? '):
        if is_random_words_included:
            GenerateRandomWords(
                Config.RANDOM_GENERATOR_MINIMUM_LENGTH,
                Config.RANDOM_GENERATOR_MAXIMUM_LENGTH
            ).generate()
        print_separator('_')
        if is_web_words_included:
            WebScraper.extract()

    if is_random_words_included:
        paths.append(Config.OUTPUT_WORDS_RANDOM_FILE)
    if is_web_words_included:
        paths.append(Config.OUTPUT_WORDS_WEB_FILE)

    if Config.DATASET_SOURCE_ORDER == DatasetSourceOrderEnum.WebWordsFirst:
        paths = paths[::-1]

    DirectoryUtil.merge_files(paths, Config.OUTPUT_WORDS_TOTAL_FILE)
    print_separator('_')
    count_generated()


def generate_images():
    dataset_generator = DatasetGenerator(
        ImageSize(
            Config.FIXED_IMG_SIZE_WIDTH,
            Config.FIXED_IMG_SIZE_HEIGHT,
        ),
    )
    is_continue = False
    if exists(Config.OUTPUT_SAVE_PROGRESS_FILE) and answer_input('Do you want to continue generating? '):
        try:
            # Check if file is valid
            ProgressUtil.retrieve_progress()
            is_continue = True
        except Exception as ex:
            print(ex.with_traceback())
            is_continue = False
    dataset_generator.generate_images(is_continue)


@print_exec_time
def main():
    DirectoryUtil.ensure_folders()
    print_separator('#')
    generate_words()
    print_separator('#')
    generate_images()
    print_separator('#')


if __name__ == "__main__":
    Debugger.init_debugger()
    main()
    print()
