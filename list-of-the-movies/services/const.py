import logging
from pathlib import Path
from typing import Final

from services.tools import get_project_root

BASE_DIR: Final[Path] = get_project_root()
DB_PATH: Final[Path] = Path(BASE_DIR / "db" / "movies.json")

LOG_LEVEL = logging.DEBUG
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
    }
)
API_TOKENS: frozenset[str] = frozenset(
    {
        "mFOcFcH4FWqEfH-88jhCTbVxN6c",
        "PkaVw5QFUmypE9Gwsf2y2g",
        "T2FP-VqUmzfg5nZ01ZxrCA",
    }
)
