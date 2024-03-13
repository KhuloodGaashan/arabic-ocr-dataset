from input.config import *
from io import TextIOWrapper
from PIL.ImageFont import FreeTypeFont
from .font_util import FontUtil
from dataclasses import dataclass


@dataclass
class Progress:
    font_name: str
    font_size: int
    progress: int


class ProgressUtil:
    SEPERATOR: str = "\n"

    @staticmethod
    def save_progress(progress: Progress) -> None:
        with open(Config.OUTPUT_SAVE_PROGRESS_FILE, 'w+') as file:
            to_write = [progress.font_name, progress.font_size, progress.progress]
            file.write("\n".join(str(w) for w in to_write))

    @staticmethod
    def retrieve_progress() -> Progress:
        with open(Config.OUTPUT_SAVE_PROGRESS_FILE, 'r') as file:
            font_name, font_size, progress = file.read().split('\n')
        progress = Progress(font_name, int(font_size), int(progress))
        return progress

    @staticmethod
    def is_identical_font(font: FreeTypeFont, progress: Progress):
        return FontUtil.get_font_name(font) == progress.font_name and \
            font.size == progress.font_size

    @staticmethod
    def apply_progress_fonts(fonts: list[FreeTypeFont],) -> int:
        progress = ProgressUtil.retrieve_progress()
        finished = 0
        for font in fonts:
            if ProgressUtil.is_identical_font(font, progress):
                break
            fonts.pop(0)
            finished += 1
        return finished

    @staticmethod
    def apply_progress_file(font: FreeTypeFont, file: TextIOWrapper) -> int:
        CHUNCK_SIZE = 1000
        progress = ProgressUtil.retrieve_progress()
        if not ProgressUtil.is_identical_font(font, progress):
            return 0
        for i in range(progress.progress//CHUNCK_SIZE):
            file.readlines(CHUNCK_SIZE)
        file.readlines(progress.progress % CHUNCK_SIZE)
        return progress.progress
