import logging
import sys

from tools.const import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    handlers=(logging.StreamHandler(sys.stdout),),
)
log = logging.getLogger()
