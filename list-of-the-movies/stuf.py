"""
Модуль для тестирования
"""

from redis import Redis
import db.redis_db.redis_config as rc

redis = Redis(
    host=rc.REDIS_HOST,
    port=rc.REDIS_PORT,
    db=rc.REDIS_DB,
    decode_responses=rc.REDIS_DECODE,
)


def main():
    print(redis.ping())
    redis.set("hello", "world")
    print("Получаем по команде GET: ", redis.get("hello"))
    redis.set("name", "Gleb")
    print("Получаем по команде GET перед удалением: ", redis.get("name"))
    redis.delete("name")
    print("Получаем по команде GET после удаления: ", redis.get("name"))


if __name__ == "__main__":
    main()
