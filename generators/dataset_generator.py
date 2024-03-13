from input.config import *
from utils.image_util import ImageUtil
from utils.font_util import FontUtil
from processes.labels_writer import LabelWriter
from utils.decorators import print_exec_time
from utils.models import *
from processes.progressbar import ProgressBar
from processes.job_worker import JobWorker
from processes.image_worker import ImageWorker
from multiprocessing import Queue, Process, Manager as ManagerCreator
import ctypes


def set_total_count(path: str) -> None:
    if Config.SAMPLES_PER_FONT_LIMIT >= 0:
        return
    Config.SAMPLES_PER_FONT_LIMIT = 0
    with open(path, 'r', encoding="utf8") as file:
        CHUNK_SIZE = 100
        while len(lines := file.readlines(CHUNK_SIZE)) > 0:
            Config.SAMPLES_PER_FONT_LIMIT += len(lines)


class DatasetGenerator(object):
    MAX_WORKERS = [1, Config.MAX_CONCURRENT_PROCESSES-3][not Config.IS_DEBUGGING]

    def __init__(self, specific_size: ImageSize = None):
        self.per_font_counter = 0
        self.image_size = ImageSize(0, 0)

        fonts = FontUtil.get_all_fonts()
        words = DatasetGenerator._get_words_sample(Config.OUTPUT_WORDS_TOTAL_FILE)
        self.image_size = ImageUtil.compute_max_text_size(words, fonts)

        self.labels_writer: LabelWriter = None
        self.job_worker: JobWorker = None
        self.image_worker: ImageWorker = None
        self.progressbar: ProgressBar = None

    @staticmethod
    def _get_words_sample(path: str) -> list[str]:
        words: list[str] = []
        with open(path, 'r', encoding='utf8') as file:
            position = file.seek(0, 2) - 600
            position = [0, position][position >= 0]
            while True:
                try:
                    file.seek(position, 0)
                    words = file.readlines()[1:]
                    break
                except:
                    position += 1
            file.seek(position, 0)
            words = file.readlines()[1:]
        return words

############################ MULTIPROCESSING ACTIVITY ############################

    @print_exec_time
    def generate_images(self, is_continue=False) -> None:
        set_total_count(Config.OUTPUT_WORDS_TOTAL_FILE)
        limit = Config.SAMPLES_PER_FONT_LIMIT
        fonts_count = len(FontUtil.get_all_fonts())
        quality_count, sizes_count, total = DatasetGenerator.calculate_expected(limit, fonts_count)
        self._start_workers(limit, total, is_continue)

        print(f'Total Images Created: {total:,} images | {Config.SAMPLES_PER_FONT_LIMIT*sizes_count*quality_count:,} images / font')
        if Config.IS_MULTI_SIZE:
            print(f'Font size: {sizes_count} size / font')
        if Config.IS_MULTI_QUALITY:
            print(f'Image Quality: {quality_count} quality / image')
        print()

    def _start_workers(self, limit: int, total: int, is_continue: bool):
        MAX_QUEUE_SIZE = 3000
        manager = ManagerCreator()

        self.labels_writer = LabelWriter(limit)
        self.job_worker = JobWorker(self.image_size, limit, is_continue)
        self.image_worker = ImageWorker()
        self.progressbar = ProgressBar(total, 'image')

        counter = manager.Value('i', 0)
        couter_lock = manager.Lock()
        done = manager.Value(ctypes.c_bool, False)
        done_lock = manager.Lock()

        worker_queue: Queue[ImageJobBuilder] = manager.Queue(MAX_QUEUE_SIZE)
        label_queue: Queue[LabelJobBuilder] = manager.Queue(MAX_QUEUE_SIZE)

        match Config.IMAGE_SAVE_METHOD:
            case ImageSaveMethodEnum.SaveAsImages:
                worker_processes = [
                    Process(
                        target=self.image_worker.create_jpg_worker,
                        args=(counter, couter_lock, worker_queue, label_queue, done),
                        name=f'worker{i}'
                    ) for i in range(max(DatasetGenerator.MAX_WORKERS, 1))
                ]
            case ImageSaveMethodEnum.SaveAsArchive:
                writer_queue: Queue[ArchiveJobBuilder] = manager.Queue(MAX_QUEUE_SIZE)
                worker_processes = [
                    *[
                        Process(
                            target=self.image_worker.create_archive_worker,
                            args=(counter, couter_lock, worker_queue, label_queue, writer_queue, done),
                            name=f'worker{i}'
                        ) for i in range(max(DatasetGenerator.MAX_WORKERS-1, 1))
                    ],
                    Process(
                        target=self.image_worker.archive_writer_worker,
                        args=(writer_queue, done),
                        name=f'archive_writer'
                    )
                ]

        processes: list[Process] = [
            Process(target=self.job_worker.job_producer, args=(counter, worker_queue, done, done_lock), name='producer'),
            Process(target=self.progressbar.print_percentage, args=(counter, done), name='progress'),
            *worker_processes,
            Process(target=self.labels_writer.write_labels, args=(label_queue, done), name="labels_writer")
        ]

        print(f'Total Images to Create: {total:,}')
        print()

        pass
        for process in processes:
            process.start()

        pass
        for process in processes:
            process.join()


##################################################################################

    @staticmethod
    def calculate_expected(limit_per_font, fonts_count):
        quality_count = [1, len(Config.IMAGE_QUALITIES)][Config.IS_MULTI_QUALITY]
        sizes_count = [1, len(Config.FONT_SIZES)][Config.IS_MULTI_SIZE]
        total = limit_per_font * fonts_count * quality_count
        return (quality_count, sizes_count, total)
