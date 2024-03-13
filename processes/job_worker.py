from input.config import *
from utils.models import *
from utils.font_util import FontUtil
from utils.progress_util import ProgressUtil
from threading import Lock
from multiprocessing import Queue
from multiprocessing.managers import ValueProxy


class JobWorker(object):
    def __init__(self, image_size: ImageSize, limit: int, is_continue: bool):
        self.image_size = image_size
        self.limit = limit
        self.is_continue = is_continue

    def job_producer(
        self,
        counter: ValueProxy[int],
        worker_queue: "Queue[ImageJobBuilder]",
        done: ValueProxy[bool],
        done_lock: Lock
    ):
        inc_size = 1
        fonts = FontUtil.get_all_fonts()
        LIMIT_PER_FONT = self.limit
        if self.is_continue:
            finished = ProgressUtil.apply_progress_fonts(fonts)
            counter.value += finished*LIMIT_PER_FONT

        for font in fonts:
            produced = 0
            with open(Config.OUTPUT_WORDS_TOTAL_FILE, 'r', encoding="utf8") as file:
                if self.is_continue:
                    produced = ProgressUtil.apply_progress_file(font, file)
                    counter.value += produced

                while True:
                    if not (word := file.readline()) or produced >= LIMIT_PER_FONT:
                        break
                    word = word.replace('\n', '')
                    options = ImageJobBuilder(word, font, self.image_size)
                    worker_queue.put(options)
                    produced += inc_size
        with done_lock:
            done.value = True
