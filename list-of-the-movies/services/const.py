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

REDIS_TOKEN_SET_NAME: Final[str] = "tokens"

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
    }
)

FAKE_USERNAME_DB: dict[str, str] = {
    "bob": "password",
    "jon": "qwerty",
}
