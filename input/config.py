from os.path import join as path_join
from multiprocessing import cpu_count
from utils.models import *


class Config(object):
    # ******************************************************************************************
    # The generated sampels can be a single PNG file for each word sample, or a singl binary file containing all samples
    # or both png files and single binary file
    IMAGE_SAVE_METHOD = ImageSaveMethodEnum.SaveAsArchive

    # Setting Dataset source
    DATASET_SOURCE = DatasetSourceEnum.RandomWordsOnly

    # Modifies the reading order of dataset source
    DATASET_SOURCE_ORDER = DatasetSourceOrderEnum.RandomWordsFirst

    # used to limit the number of generated samples per font
    # specify a number of set to 0 or -1 to process all samples in base file
    # use in DatasetGenerator.RotateThroughFonts()
    SAMPLES_PER_FONT_LIMIT = 500000

    # max number of processes that runs simultaneously
    # for a specific task
    MAX_CONCURRENT_PROCESSES = cpu_count()

    # ******************************************************************************************
    #                                       CONFIGUATIONS
    # ******************************************************************************************

    RANDOM_GENERATOR_MINIMUM_LENGTH = 4
    RANDOM_GENERATOR_MAXIMUM_LENGTH = 4

    FIXED_IMG_SIZE_HEIGHT = 32
    FIXED_IMG_SIZE_WIDTH = 128

    # Turn on Is with Diacritics Feature
    IS_WITH_DIACRITICS = True

    # Turn on Multi Font Size Feature
    IS_MULTI_SIZE = False
    FONT_SIZES = [20, 18, 16, 12]
    DEFAULT_FONT_SIZE = 26

    # Turn on Multi Quality Feature
    IS_MULTI_QUALITY = False
    IMAGE_QUALITIES = [100, 95]
    DEFAULT_QUALITY = 100

    # Turn on when you want to Debug
    IS_DEBUGGING = False

    # Turn on when you want to Debug
    CLEAN_DELETE_GENERATED_IMAGES = True

    # Turn on Multi Stroke Feature
    # IS_MULTI_STROKE = False
    # STROKES = [1, 2, 3]
    # DEFAULT_STROKE = 1

    # To use with multiprocessing queue timeout
    TIMEOUT_TIME = 0.1

    FONT_ITALIC = False
    RANDOMIZE_FONT_STYLE = True  # for ResizeToFitFixedBoundary only

    # ******************************************************************************************
    #                                          PATHS
    # ******************************************************************************************

    # Paths
    BASE_PATH = "./"
    INPUT_PATH = path_join(BASE_PATH, "input")
    OUTPUT_PATH = path_join(BASE_PATH, "output")

    OUTPUT_LABELS_PATH = path_join(OUTPUT_PATH, "labels")
    OUTPUT_IMAGES_PATH = path_join(OUTPUT_PATH, "images")
    OUTPUT_WORDS_PATH = path_join(OUTPUT_PATH, "words")
    OUTPUT_EXTRACT_PATH = OUTPUT_IMAGES_PATH
    INPUT_FONTS_PATH = path_join(INPUT_PATH, "fonts")
    INPUT_SCRAPER_CONFIG_PATH = path_join(INPUT_PATH, "scraper_config")

    # Files
    INPUT_WEB_GEN_FILE = path_join(INPUT_SCRAPER_CONFIG_PATH, "websites_generator.json")
    INPUT_WEB_FILE = path_join(INPUT_SCRAPER_CONFIG_PATH, "websites.json")

    OUTPUT_WORDS_RANDOM_FILE = path_join(OUTPUT_WORDS_PATH, "random_words.txt")
    OUTPUT_WORDS_WEB_FILE = path_join(OUTPUT_WORDS_PATH, "web_words.txt")
    OUTPUT_WORDS_TOTAL_FILE = path_join(OUTPUT_WORDS_PATH, "total_words.txt")
    OUTPUT_LETTERS_COUNT_FILE = path_join(OUTPUT_WORDS_PATH, "count.txt")
    OUTPUT_LABELS_FILE = path_join(OUTPUT_LABELS_PATH, "labels.csv")
    OUTPUT_IMAGES_BIN_FILE = path_join(OUTPUT_IMAGES_PATH, "images.bin")
    OUTPUT_SAVE_PROGRESS_FILE = path_join(OUTPUT_PATH, "save_progress.sav")

    # Tools
    COUNTER_PROGRAM = path_join(BASE_PATH, "counter/bin/Debug/net8.0/counter.exe")
