import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Эта абстракция создает контракт для следующих действий:
    - Проверка токена: token_exists
    - Добавления токена: add_token
    - Генерации токена: generate_and_save_token
    """

    @abstractmethod
    def token_exists(self, token_to_check: str) -> bool:
        """
        Проверяет существует ли токен в БД
        :param token_to_check: Строка, которую ищем в БД
        :return: boll значение "существует ли"
        """
        pass

    @abstractmethod
    def add_token(self, token_to_add: str) -> None:
        """
        Добавляем токен в БД
        :param token_to_add: Строка, которую необходимо добавить
        :return: None
        """
        pass

    @classmethod
    def generate_token(cls, token_size_bytes: int) -> str:
        """
        Генерирует токен с помощью библиотеки secrets
        :param token_size_bytes: Длина генерируемого токена, по-умолчанию 16 байт
        :return: Готовый токен
        """
        return secrets.token_urlsafe(token_size_bytes)

    def generate_and_save_token(self, token_size_bytes: int = 16):
        token = self.generate_token(token_size_bytes=token_size_bytes)
        self.add_token(token_to_add=token)
        return token
