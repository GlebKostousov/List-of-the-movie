from fastapi import BackgroundTasks
from crud.crud import storage
import logging

log = logging.getLogger()


def storage_save_state_background(
    background_tasks: BackgroundTasks,
):
    yield
    log.debug("Запустил фоновую задачу сохранения БД")
    background_tasks.add_task(storage.save_state)
