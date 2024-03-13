from __future__ import annotations
from input.config import *
from urllib.parse import urljoin
import json


class WebsiteDetails(object):
    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def _read_file() -> list[str]:
        with open(Config.INPUT_WEB_FILE, 'r+', encoding='utf8') as file:
            try:
                websites: list[str] = json.loads(file.read())
            except:
                raise SyntaxError(f"THERE WAS AN ERROR IN '{Config.INPUT_WEB_FILE}'!")
        return websites

    @staticmethod
    def from_file() -> list[WebsiteDetails]:
        try:
            websites = WebsiteDetails._read_file()
            details: list[WebsiteDetails] = []
            for website in websites:
                details.append(WebsiteDetails(website))
        except Exception as e:
            raise e
        return details

    @staticmethod
    def generate_to_file(domain: str, path_pattern: str, start: int, count: int) -> None:
        urls: list[str] = []
        for id in range(start, start + count):
            urls.append(urljoin(domain, path_pattern.format(id)))
        WebsiteDetails.add_to_file(urls)

    @staticmethod
    def add_to_file(urls: list[str]) -> None:
        details = WebsiteDetails._read_file()
        details = list(set(details+urls))
        with open(Config.INPUT_WEB_FILE, 'w+') as file:
            dump = json.dumps(details, ensure_ascii=False)
            file.write(dump)
