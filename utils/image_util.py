from input.config import *
from PIL import ImageDraw, Image
from PIL.ImageFont import FreeTypeFont
from io import TextIOWrapper
import math


class ImageUtil(object):
    @staticmethod
    def create_image_from_text(options: ImageJobBuilder) -> Image.Image:
        size = options.size
        image = Image.new("L", (size.width, size.height), 255)  # Image.TYPE_BYTE_GRAY
        drawer = ImageDraw.Draw(image)
        drawer.text(
            (size.width/2, size.height/2),
            options.word,
            font=options.font,
            anchor='mm',
            direction='ltr',
        )
        return image

    @staticmethod
    def append_image(image: Image.Image, fp: TextIOWrapper, quality: int = None) -> None:
        if quality:
            image.save(fp, format='jpeg', quality=quality)
        else:
            image.save(fp, format='jpeg')

    @staticmethod
    def save_image(image: Image.Image, name: str, quality: int = None) -> None:
        if quality:
            image.save(name, quality=quality)
        else:
            image.save(name)

    @staticmethod
    def resize_image(image: Image.Image, target_size) -> Image.Image:
        image.resize((target_size.width, target_size.height))
        return image

    @staticmethod
    def compute_max_text_size(words: list[str], fonts: list[FreeTypeFont]) -> ImageSize:
        max_width = 0
        max_height = 0
        for word in words:
            for font in fonts:
                size = ImageUtil.compute_text_size(word, font)

                if size.width > max_width:
                    max_width = size.width

                if size.height > max_height:
                    max_height = size.height

        UNIT = 50
        max_width = math.ceil(max_width/UNIT)*UNIT
        max_height = math.ceil(max_height/UNIT)*UNIT
        return ImageSize(max_width, max_height)

    @staticmethod
    def compute_text_size(word: str, font: FreeTypeFont) -> ImageSize:
        ascent, descent = font.getmetrics()
        width = font.getbbox(word)[2]
        height = font.getbbox(word)[3] + descent

        image_size = ImageSize(width, height)
        return image_size

    @staticmethod
    def get_max_fitting_size(options: ImageJobBuilder) -> int:
        font = options.font
        size = options.size
        word = options.word
        min_size = 0
        max_size = 288
        cur_size = font.size

        while max_size - min_size > 2:
            ascent, descent = font.getmetrics()
            font_width = font.getbbox(word)[2]
            font_height = font.getbbox(word)[3] + ascent + descent

            if font_width > size.width or font_height > size.height:
                max_size = cur_size
                cur_size = (max_size + min_size) / 2
            else:
                min_size = cur_size
                cur_size = (min_size + max_size) / 2

        return cur_size
