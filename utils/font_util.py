from input.config import *
from PIL import ImageFont
import os


class FontUtil(object):
    @staticmethod
    def get_all_fonts() -> list[ImageFont.FreeTypeFont]:
        fonts: list[ImageFont.FreeTypeFont] = []

        for file in os.scandir(Config.INPUT_FONTS_PATH):
            if file.is_file():
                try:
                    sizes = [[Config.DEFAULT_FONT_SIZE], Config.FONT_SIZES][Config.IS_MULTI_SIZE]
                    for font_size in sizes:
                        font = FontUtil.create_font(file.path, font_size)
                        fonts.append(font)
                except Exception as ex:
                    print()
                    print(f"Failed font creation {ex}")
                    print()

        return fonts

    @staticmethod
    def create_font(file_name: str, font_size: int):
        return ImageFont.truetype(file_name, font_size)

    @staticmethod
    def get_font_name(font: ImageFont.FreeTypeFont) -> str:
        return font.getname()[0]


if __name__ == "__main__":
    print(FontUtil.get_all_fonts())
