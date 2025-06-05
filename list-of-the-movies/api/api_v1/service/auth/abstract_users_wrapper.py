from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    Эта абстракция создает контракт для следующих действий:
    - Проверка пароля у пользователя
    - Добавления логина и пароля для пользователя
    """

    @abstractmethod
    def get_password_from_db(self, username: str) -> str | None:
        """
        Метод для переопределения.
        Метод получает пароль по username
        :param username:
        :return: Возвращаем пароль, если он есть, иначе None
        """

    @classmethod
    def compare_passwords(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        return password1 == password2

    @abstractmethod
    def add_username_and_password_to_db(
        self,
        username_to_add: str,
        password_to_add: str,
    ) -> None:
        """
        Метод для переопределения. Задача добавить пользователя в базу данных
        :param username_to_add: Имя пользователя для добавления
        :param password_to_add: Пароль пользователя для добавления
        """

    def verified_password_is_correct(
        self,
        username_in: str,
        password_in: str,
    ) -> bool:
        password = self.get_password_from_db(username_in)
        if password:
            return self.compare_passwords(password_in, password)

        return False
