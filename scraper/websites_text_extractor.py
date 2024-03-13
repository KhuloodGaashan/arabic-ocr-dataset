from __future__ import annotations
from input.config import Config
from .website_details import WebsiteDetails
from .website_text_extractor import WebsiteTextExtractor
from processes.progressbar import ProgressBar
from queue import Empty as EmptyException
from multiprocessing.synchronize import Semaphore
from multiprocessing.managers import ListProxy, ValueProxy
from multiprocessing import Semaphore as SemaphoreCreator, Manager as ManagerCreator, Process, Queue
from threading import Lock
import ctypes


class WebsitesTextExtractor(object):
    def __init__(self, websites: list[WebsiteDetails], workers_count: int) -> None:
        self.websites = websites
        self.workers_count = workers_count
        self.progressbar: ProgressBar

    @staticmethod
    def _extract_core(url: str, outputs: list[str]) -> str:
        extractor = WebsiteTextExtractor(url)
        outputs.append(extractor.extract())

    @staticmethod
    def _extraction_worker(inputs: Queue, counter: ValueProxy, outputs: ListProxy[str], is_finished: ValueProxy, lock: Lock) -> str:
        while True:
            try:
                detail: WebsiteDetails = inputs.get(timeout=Config.TIMEOUT_TIME)
                WebsitesTextExtractor._extract_core(detail.url, outputs)
                with lock:
                    counter.value += 1
            except EmptyException:
                break
        is_finished.value = True

    def extract_con(self) -> str:
        total: int = len(self.websites)
        manager = ManagerCreator()
        lock = manager.Lock()
        outputs = manager.list()
        inputs = manager.Queue()
        counter = manager.Value('i', 0)
        is_finished = manager.Value(ctypes.c_bool, False)

        self.progressbar = ProgressBar(total, 'website')

        processes: list[Process] = [
            Process(target=self.progressbar.print_percentage, args=(counter, is_finished)),
            *[Process(target=WebsitesTextExtractor._extraction_worker, args=(inputs, counter, outputs, is_finished, lock)) for _ in range(self.workers_count)]
        ]

        for detail in self.websites:
            inputs.put_nowait(detail)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        return ''.join(outputs)

    def extract(self) -> str:
        outputs = []
        for detail in self.websites:
            WebsitesTextExtractor._extract_core(detail.url, outputs)
        return ''.join(outputs)
