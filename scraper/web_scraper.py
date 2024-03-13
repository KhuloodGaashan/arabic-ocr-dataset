from __future__ import annotations
from input.config import *
from utils.decorators import print_exec_time
from scraper.website_details import WebsiteDetails
from scraper.websites_text_extractor import WebsitesTextExtractor
import json

# coding: utf-8


class WebScraper(object):
    @print_exec_time
    @staticmethod
    def extract():
        process_count = Config.MAX_CONCURRENT_PROCESSES
        with open(Config.INPUT_WEB_GEN_FILE, 'r+', encoding='utf8') as file:
            websites_gen_info: list[dict] = json.loads(file.read())

        for info in websites_gen_info:
            WebsiteDetails.generate_to_file(*info.values())

        websites = WebsiteDetails.from_file()
        extractor = WebsitesTextExtractor(websites, process_count)
        content = extractor.extract_con()

        with open(Config.OUTPUT_WORDS_WEB_FILE, "w+", encoding="utf8") as file:
            file.write(content)

        print(f'Websites Scraped: {len(websites)} website')


if __name__ == "__main__":
    WebScraper.extract()
