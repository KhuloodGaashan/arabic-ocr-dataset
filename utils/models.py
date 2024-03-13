from dataclasses import dataclass
from PIL.ImageFont import FreeTypeFont
from PIL.Image import Image
from enum import Enum


@dataclass
class ImageSize:
    width: int
    height: int


@dataclass
class JobBuilder:
    pass


@dataclass
class LabelJobBuilder(JobBuilder):
    word: str
    image_size: ImageSize
    font_name: str
    font_size: int
    quality: int
    image_name: str


@dataclass
class ImageJobBuilder(JobBuilder):
    word: str
    font: FreeTypeFont
    size: ImageSize


@dataclass
class ArchiveJobBuilder(JobBuilder):
    image_name: str
    image: Image
    quality: int


class ImageSaveMethodEnum(Enum):
    SaveAsImages = 0
    SaveAsArchive = 1


class DatasetSourceEnum(Enum):
    WebWordsOnly = 0
    RandomWordsOnly = 1
    Both = 2


class DatasetSourceOrderEnum(Enum):
    WebWordsFirst = 1
    RandomWordsFirst = 2
