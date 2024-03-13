from __future__ import annotations
from input.config import *
from multiprocessing import log_to_stderr, get_logger
from utils.decorators import *
from utils.models import *
from utils.font_util import FontUtil
from processes.job_worker import JobWorker
from processes.image_worker import ImageWorker
from generators.dataset_generator import DatasetGenerator
import logging
import os


@dataclass
class ValueProxyDebug:
    value = 0


class LockDebug:
    def __enter__(self):
        return

    def __exit__(self, a, b, c):
        return


class QueueDebug:
    def __init__(self):
        self._queue = []

    def put(self, data, timeout=0):
        self._queue.append(data)

    def get(self, timeout=0):
        return self._queue.pop(0)

    def qsize(self):
        return len(self._queue)


@print_debug_name
def debug_fonts():
    fonts = FontUtil.get_all_fonts()
    for font in fonts:
        print(f"\t{font.getname()[0]} -> {font.size}")
    print(f"\tTotal of {len(fonts)} fonts")


@print_debug_name
def debug_create_image():
    font = FontUtil.get_all_fonts()[0]
    quality_count, sizes_count, total = DatasetGenerator.calculate_expected(1, 1)
    Config.IS_DEBUGGING = False
    ImageWorker().create_jpg_worker(
        ValueProxyDebug(),
        ImageJobBuilder('Hello', font, ImageSize(200, 200)),
        QueueDebug()
    )
    count = len(list(os.scandir(Config.OUTPUT_IMAGES_PATH)))
    if count != total:
        print(f"\tFAILED [qsize({count}) != jobs({total})]")
    else:
        print(f"\tCORRECT [qsize({count}) == jobs({total})]")


@print_debug_name
def debug_job_producer():
    fonts = FontUtil.get_all_fonts()
    Config.IS_DEBUGGING = False
    mul = [1, len(Config.IMAGE_QUALITIES)][Config.IS_MULTI_QUALITY]
    is_continue = False
    limit = 100
    quality_count, sizes_count, total = DatasetGenerator.calculate_expected(limit, len(fonts))

    worker_queue = QueueDebug()
    JobWorker().job_producer(is_continue, limit, worker_queue, ValueProxyDebug[bool], LockDebug())
    size = worker_queue.qsize()*mul

    if size != total:
        print(f"\tFAILED [qsize({size}) != jobs({total})]")
    else:
        print(f"\tCORRECT [qsize({size}) == jobs({total})]")


class Debugger(object):
    DEBUG_METHODS_RUN: list = [
        debug_fonts,
        debug_create_image,
        debug_job_producer
    ]

    @staticmethod
    def init_debugger():
        if not Config.IS_DEBUGGING:
            return

        for method in Debugger.DEBUG_METHODS_RUN:
            method()

        exit()
        return
        log_to_stderr()
        logger = get_logger()
        logger.setLevel(logging.DEBUG)
