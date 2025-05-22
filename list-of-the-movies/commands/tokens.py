from typing import Annotated

import redis
import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.service.auth.redis_auth import redis_token

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Управление токенами",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="Токен для проверки"),
    ],
) -> None:
    """
    Проверяет валидность токена
    """
    print(
        f"[bold]token: {token}[/bold]",
        (
            "[green]exists[/green]"
            if redis_token.token_exists(token)
            else "[red]doesn't exist[/red]"
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    Печать списка всех доступных токенов
    """
    print(Markdown("# **Available API tokens**"))
    print(Markdown("\n- ".join([""] + redis_token.get_all_tokens())))
    print()


@app.command()
def rm(token_to_delete) -> None:
    """
    Удаляет токен из БД, если он существует
    """
    if redis_token.token_exists(token_to_delete):
        redis_token.delete_token(token_to_delete)
        print("[green]token deleted[/green]")
        return

    print("[red]token doesn't exist[/red]")


@app.command()
def create(
    token_size_bytes: Annotated[
        int,
        typer.Argument(help="Размер токена"),
    ] = 16,
) -> None:
    """
    Создает новый токен и добавляет его в БД
    """
    if redis_token.generate_and_save_token(token_size_bytes=token_size_bytes):
        print("[green]Токен создан[/green]")
        return

    print("[red]Ошибка при создании токена[/red]")


@app.command()
def add(
    token_to_add: Annotated[
        str,
        typer.Argument(help="Токен для добавления в БД"),
    ],
) -> None:
    """
    Добавляет токен, который передается аргументом
    """
    try:
        redis_token.add_token(token_to_add=token_to_add)
        print(f"[green]Токен: {token_to_add} успешно добавлен![/green]")
    except redis.exceptions.ResponseError:
        print("[red]Ошибка при добавлении токена![/red]")
