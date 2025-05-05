from pathlib import Path


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
