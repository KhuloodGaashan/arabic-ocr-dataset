from input.config import *
import os
import shutil


class DirectoryUtil(object):
    @staticmethod
    def delete_directory_content(path: str) -> None:
        print("Deleteing directories content...")

        if not DirectoryUtil.ensure_created(path):
            return

        if os.path.isdir(path):
            shutil.rmtree(path, True)
            # for file in os.scandir(path):
            #     os.remove(file)
            if not os.path.exists(path):
                os.mkdir(path)

    @staticmethod
    def ensure_created(path: str) -> bool:
        if not os.path.exists(path):
            os.mkdir(path)
            return False
        return True

    @staticmethod
    def ensure_folders():
        DirectoryUtil.ensure_created(Config.INPUT_PATH)
        DirectoryUtil.ensure_created(Config.OUTPUT_PATH)
        DirectoryUtil.ensure_created(Config.OUTPUT_IMAGES_PATH)
        DirectoryUtil.ensure_created(Config.OUTPUT_LABELS_PATH)
        DirectoryUtil.ensure_created(Config.OUTPUT_WORDS_PATH)
        if Config.CLEAN_DELETE_GENERATED_IMAGES:
            DirectoryUtil.delete_directory_content(Config.OUTPUT_IMAGES_PATH)
            DirectoryUtil.delete_directory_content(Config.OUTPUT_LABELS_PATH)
            DirectoryUtil.delete_file(Config.OUTPUT_SAVE_PROGRESS_FILE)

    @staticmethod
    def delete_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def merge_files(paths: list[str], output_path: str) -> None:
        with open(output_path, 'wb') as output_file:
            for path in paths:
                with open(path, 'rb') as input_file:
                    shutil.copyfileobj(input_file, output_file)
