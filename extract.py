from input.config import Config
from utils.archive_util import ArchiveUtil

ArchiveUtil.extract(Config.OUTPUT_IMAGES_BIN_FILE, Config.OUTPUT_EXTRACT_PATH)
