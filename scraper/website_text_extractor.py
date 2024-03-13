from __future__ import annotations
from bs4 import BeautifulSoup
import requests
import re


class WebsiteTextExtractor(object):
    def __init__(self, url: str) -> None:
        self.url = url
        self.query = 'body'

    @staticmethod
    def filter(text: str) -> str:
        return '\n'.join(re.findall(r"[\u0600-\u06FF0-9]+", text, re.UNICODE))

    def extract_text(self) -> str:
        r = requests.get(self.url)
        bs = BeautifulSoup(r.content, "html.parser")
        container = bs.select_one(self.query)
        if container:
            return WebsiteTextExtractor.filter(container.text)
        else:
            return ""

    def split_text_to_words(self, text: str) -> str:
        words = list(set([w.strip() for w in text.replace("\r\n", " ").replace("\n", " ").split(" ") if w.strip()]))
        return "\n".join(words)+"\n"

    def extract(self) -> str:
        text = self.extract_text()
        if not text:
            return text
        return self.split_text_to_words(text)


if __name__ == "__main__":
    print(WebsiteTextExtractor('https://www.aldiwan.net/poem25902.html').extract())
