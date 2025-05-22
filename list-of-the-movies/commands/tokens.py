from typing import Annotated

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
