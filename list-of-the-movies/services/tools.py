from pathlib import Path
import sys


# from typing import Type
# import json
# from pydantic import BaseModel
#
#
def get_project_root() -> Path:
    """
    Находит корень проекта через файл main.py в родительских директориях.
    """
    current_file = Path(__file__).resolve()
    root = current_file
    while True:
        if (root / "main.py").exists():  # Проверяем наличие main.py
            return root
        parent = root.parent
        if parent == root:  # Достигли корня файловой системы
            raise FileNotFoundError("Файл main.py не найден.")
        root = parent


#
#
# def save_to_json(data: Type[BaseModel], file: str) -> None:
#     """
#     Сохраняет данные в JSON-файл.
#     Если данные являются датаклассом, они преобразуются в словарь с помощью asdict.
#
#     """
#     # Добавляем расширение .json к имени файла
#     file += ".json"
#
#     # Получаем корневой путь проекта
#     root = get_project_root()
#     file_path = root / file
#
#     try:
#         with data.model_dump_json(...) as json_file:
#         # with open(file_path, "w", encoding="utf-8") as json_file:
#         #     json.dump(data, json_file, ensure_ascii=False, indent=4)
#
#     except Exception as e:
#         raise
