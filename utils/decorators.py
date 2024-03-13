from typing import Callable
import time


def print_exec_time(func: Callable) -> Callable:
    def wrap_func(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        total = t2-t1
        time_format = time.strftime('%H:%M:%S', time.gmtime(total))
        print(f'Time elapsed: {time_format}')
        return result
    return wrap_func


def exit_after_debug(func: Callable) -> Callable:
    def wrap_func(*args, **kwargs):
        func(*args, **kwargs)
        exit()
    return wrap_func


def print_debug_name(func: Callable) -> Callable:
    def wrap_func(*args, **kwargs):
        print(f"{func.__name__.upper()} OUTPUT:")
        func(*args, **kwargs)
        print()
    return wrap_func
