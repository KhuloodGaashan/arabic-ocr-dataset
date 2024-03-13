from utils.models import *
from utils.font_util import FontUtil
from utils.image_util import ImageUtil
from utils.archive_util import ArchiveUtil
from queue import Empty as EmptyException
from multiprocessing import Queue
from multiprocessing.managers import ValueProxy
from threading import Lock
from input.config import *
import time


class ImageWorker:
    def __init__(self) -> None:
        pass

    def create_jpg_worker(
        self,
        counter: ValueProxy[int],
        counter_lock: Lock,
        worker_queue: "Queue[ImageJobBuilder]",
        label_queue: "Queue[LabelJobBuilder]",
        done: ValueProxy[bool]
    ):
        inc_size = [1, len(Config.IMAGE_QUALITIES)][Config.IS_MULTI_QUALITY]
        MAX_EXCEPTIONS_ALLOWED = 3
        while True:
            try:
                options = worker_queue.get(timeout=Config.TIMEOUT_TIME)
                self._create_png(options, label_queue)
                with counter_lock:
                    counter.value += inc_size
            except EmptyException:
                MAX_EXCEPTIONS_ALLOWED -= 1
                if MAX_EXCEPTIONS_ALLOWED <= 0 and done.value:
                    break
            except Exception as ex:
                print(ex.with_traceback())
                if Config.IS_DEBUGGING:
                    exit()

    def create_archive_worker(
        self,
        counter: ValueProxy[int],
        counter_lock: Lock,
        worker_queue: "Queue[ImageJobBuilder]",
        label_queue: "Queue[LabelJobBuilder]",
        writer_queue: "Queue[ArchiveJobBuilder]",
        done: ValueProxy[bool]
    ):
        inc_size = [1, len(Config.IMAGE_QUALITIES)][Config.IS_MULTI_QUALITY]
        MAX_EXCEPTIONS_ALLOWED = 3
        while True:
            try:
                options = worker_queue.get(timeout=Config.TIMEOUT_TIME)
                self._add_to_archive(options, label_queue, writer_queue)
                with counter_lock:
                    counter.value += inc_size
            except EmptyException:
                MAX_EXCEPTIONS_ALLOWED -= 1
                if MAX_EXCEPTIONS_ALLOWED <= 0 and done.value:
                    break
            except Exception as ex:
                print(ex.with_traceback())
                if Config.IS_DEBUGGING:
                    exit()

    def _add_to_archive(self, options: ImageJobBuilder, label_queue: "Queue[LabelJobBuilder]", writer_queue: "Queue[ArchiveJobBuilder]"):
        if Config.IS_DEBUGGING:
            time.sleep(0.01)
            return

        MAX_WORD_LENGTH = 12
        image = ImageUtil.create_image_from_text(options)
        mod_word = options.word+'\0'*(MAX_WORD_LENGTH-len(options.word))
        hex_word = ''.join(f'{ord(mod_word[c]):02x}' for c in range(MAX_WORD_LENGTH))

        qualities = [[Config.DEFAULT_QUALITY], Config.IMAGE_QUALITIES][Config.IS_MULTI_QUALITY]
        for quality in qualities:
            font_name = FontUtil.get_font_name(options.font)
            font_size = options.font.size
            image_name = f'{font_name}_{hex_word}_{font_size}px_{quality}.jpg'
            writer_job = ArchiveJobBuilder(image_name, image, quality)
            writer_queue.put(writer_job)
            label_job = LabelJobBuilder(
                options.word,
                options.size,
                font_name,
                font_size,
                quality,
                image_name
            )
            label_queue.put(label_job)

    def archive_writer_worker(self, writer_queue: "Queue[ArchiveJobBuilder]", done: ValueProxy[bool]):
        MAX_EXCEPTIONS_ALLOWED = 3
        ArchiveUtil.create_archive()
        with open(Config.OUTPUT_IMAGES_BIN_FILE, 'ab+') as file:
            while True:
                try:
                    job = writer_queue.get(timeout=Config.TIMEOUT_TIME)
                    ArchiveUtil.add_to_archive(file, job)
                except EmptyException:
                    MAX_EXCEPTIONS_ALLOWED -= 1
                    if MAX_EXCEPTIONS_ALLOWED <= 0 and done.value:
                        break

    def _create_png(self, options: ImageJobBuilder, label_queue: "Queue[LabelJobBuilder]"):
        if Config.IS_DEBUGGING:
            time.sleep(0.01)
            return

        MAX_WORD_LENGTH = 12
        image = ImageUtil.create_image_from_text(options)
        mod_word = options.word+'\0'*(MAX_WORD_LENGTH-len(options.word))
        hex_word = ''.join(f'{ord(mod_word[c]):02x}' for c in range(MAX_WORD_LENGTH))

        qualities = [[Config.DEFAULT_QUALITY], Config.IMAGE_QUALITIES][Config.IS_MULTI_QUALITY]
        for quality in qualities:
            font_name = FontUtil.get_font_name(options.font)
            font_size = options.font.size
            image_name = f'{font_name}_{hex_word}_{font_size}px_{quality}.jpg'
            path = path_join(Config.OUTPUT_IMAGES_PATH, image_name)
            ImageUtil.save_image(image, path, quality)
            label_options = LabelJobBuilder(
                options.word,
                options.size,
                font_name,
                font_size,
                quality,
                image_name
            )
            label_queue.put(label_options)
