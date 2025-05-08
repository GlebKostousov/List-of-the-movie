from fastapi import BackgroundTasks, Request
from crud.crud import storage
from services.const import UNSAFE_METHODS
import logging

log = logging.getLogger()


def storage_save_state_background(
    background_tasks: BackgroundTasks,
    request: Request,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Запустил фоновую задачу сохранения БД")
        background_tasks.add_task(storage.save_state)
