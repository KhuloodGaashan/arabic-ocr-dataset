from input.config import Config
from io import TextIOWrapper
from .models import ArchiveJobBuilder
from .image_util import ImageUtil
import sys
import os


class ArchiveUtil:
    END_OF_FILE = rb"\x00\x00EOF\x00\x00"
    END_OF_ELEMENT = rb"\x00\x00EOE\x00\x00"
    CHUNCK_SIZE = 1024*1024

    @staticmethod
    def create_archive() -> None:
        with open(Config.OUTPUT_IMAGES_BIN_FILE, 'ab+') as file:
            pass

    @staticmethod
    def add_to_archive(file: TextIOWrapper, job: ArchiveJobBuilder) -> None:
        file.write(bytes(job.image_name, encoding='utf8'))
        file.write(ArchiveUtil.END_OF_ELEMENT)
        ImageUtil.append_image(job.image, file, job.quality)
        file.write(ArchiveUtil.END_OF_FILE)

    @staticmethod
    def extract(archive_path: str, extract_path: str) -> None:
        buffer = b''
        REFRESH_RATE = 1000
        created_images = 0
        with open(archive_path, 'rb') as file:
            while (content := file.read(ArchiveUtil.CHUNCK_SIZE)):
                buffer += content
                *packets, content = buffer.split(ArchiveUtil.END_OF_FILE)
                for packet in packets:
                    name, image = packet.split(ArchiveUtil.END_OF_ELEMENT)
                    name = name.decode()
                    path = os.path.join(extract_path, name)
                    with open(path, 'wb+') as new_image:
                        new_image.write(image)
                    created_images += 1
                buffer = content
                if created_images % REFRESH_RATE == 0:
                    sys.stdout.flush()
                    sys.stdout.write(f'\r{created_images} images created \r')
        sys.stdout.flush()
        sys.stdout.write(f'\r{created_images} images created \r')
        print('\n')
