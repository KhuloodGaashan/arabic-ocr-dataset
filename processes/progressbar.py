from input.config import *
from multiprocessing.managers import ValueProxy
from datetime import datetime, timedelta
from os import get_terminal_size
import sys
import time


class ProgressBar(object):
    def __init__(self, total: int, unit_name: str):
        self.total = total
        self.unit_name = unit_name

    @staticmethod
    def format_time(secs: float, decimals: int = 2) -> str:
        if secs < 360:
            return f"{secs: .0{decimals}f} s"
        sec = timedelta(seconds=secs)
        span = datetime(1, 1, 1) + sec
        values = [
            span.year-1,
            span.month-1,
            span.day-1,
            span.hour,
            span.minute,
        ]
        final = f'{span.second:02}'
        index = 0
        while index < len(values) and values[index] <= 0:
            index += 1
        for val in values[index:][::-1]:
            final = f"{val:02}:{final}"
        return final

    def print_percentage(self, counter: ValueProxy[int], done: ValueProxy[bool]):
        current = 0
        start_time = time.perf_counter()
        clearer = ' '*5
        unit = f'{self.unit_name} / s'

        def progressbar(iteration, total):
            prefix = '['
            suffix = ']'
            decimals = 1
            length = 60
            fill = '█'
            loading = ['/', '|', '\\', '-']

            def print_progress_bar(iteration):
                loader = ['', loading[current % len(loading)]+' '][iteration != total]
                percent = 100.0 * float(iteration / total)
                filled_length = int(length * (iteration / total))
                bar = fill * filled_length + '-' * (length - filled_length)
                speed = max(iteration / (time.perf_counter() - start_time), 1)
                rest = (total-iteration)/speed

                progressbar_format = f"| {bar} |"
                loader_format = f"{loader}{percent: .0{decimals}f}%"
                speed_format = f"{speed: .{decimals}f} {unit}"
                estimated_format = ProgressBar.format_time(rest, decimals)
                sys.stdout.flush()
                sys.stdout.write(f'\r{prefix} {progressbar_format} {loader_format} | {speed_format} | {estimated_format} {suffix}{clearer} \r')

            print_progress_bar(iteration)

        while counter.value < self.total:
            progressbar(counter.value, self.total)
            time.sleep(0.1)
            current += 1
            if done.value == True:
                counter.value = self.total
        progressbar(self.total, self.total)
        print('\n')
