import typer
from typing import Annotated
from rich import print


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(help="Приветствуем пользователя по имени")
def hello(
    name: Annotated[
        str,
        typer.Argument(
            help="Имя для приветствия",
        ),
    ],
) -> None:
    print(f"[bold]Hello, [green]{name}[/green]![/bold]!")
