from input.config import *
from utils.models import *
from utils.progress_util import *
from multiprocessing.managers import ValueProxy
from multiprocessing.queues import Queue
from queue import Empty as EmptyException
import atexit


class LabelWriter(object):
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.jobs: list[LabelJobBuilder] = []
        self.counter: int = 0
        self.jobs_queue: "Queue[LabelJobBuilder]"
        with open(Config.OUTPUT_LABELS_FILE, 'a+', encoding='utf-8-sig') as file:
            content = f"word, width, height, font_name, font_size, quality, name"
            file.write(content+'\n')

    def __exit(self):
        if len(self.jobs) > 0:
            self.write_to_csv(self.jobs)
            options = self.jobs[-1]
            ProgressUtil.save_progress(Progress(options.font_name, options.font_size, self.counter))
            self.jobs.clear()

    def write_to_csv(self, contents: list[LabelJobBuilder]) -> None:
        with open(Config.OUTPUT_LABELS_FILE, 'a+', encoding='utf-8-sig') as file:
            content = '\n'.join(', '.join(str(prop) for prop in props.__dict__.values()) for props in contents)
            file.write(content+'\n')

    def write_labels(self, label_queue: "Queue[LabelJobBuilder]", done: ValueProxy[bool]):
        atexit.register(self.__exit)
        self.jobs_queue = label_queue
        try:
            self._write_labels(done)
        except Exception as ex:
            print(ex.with_traceback())

    def _write_labels(self, done: ValueProxy[bool]):
        CHUNK_SIZE = 3000
        MAX_EXCEPTIONS_ALLOWED = 3
        while True:
            try:
                self.jobs.append(self.jobs_queue.get(timeout=.1))
                self.counter = (self.counter + 1) % self.limit
            except EmptyException:
                MAX_EXCEPTIONS_ALLOWED -= 1
                if MAX_EXCEPTIONS_ALLOWED <= 0 and done.value:
                    break
            except Exception as ex:
                print(ex.with_traceback())
            if len(self.jobs) >= CHUNK_SIZE:
                self.write_to_csv(self.jobs)
                options = self.jobs[-1]
                ProgressUtil.save_progress(Progress(options.font_name, options.font_size, self.counter))
                self.jobs.clear()
        if len(self.jobs) > 0:
            self.write_to_csv(self.jobs)
            options = self.jobs[-1]
            ProgressUtil.save_progress(Progress(options.font_name, options.font_size, self.counter))
            self.jobs.clear()
