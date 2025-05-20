import logging
from typing import Final

LOG_LEVEL = logging.DEBUG
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

UNSAFE_METHODS: Final[list[str]] = [
    "PUT",
    "DELETE",
    "POST",
    "PATCH",
]
