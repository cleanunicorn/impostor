import click
from flows.impostor_flow import create_flow_impostor


@click.group()
def main():
    """Impostor game."""
    pass


@main.command()
@click.option(
    "--players",
    required=False,
    default=6,
    type=int,
    help="Number of players in the game.",
)
@click.option(
    "--add-human",
    is_flag=True,
    help="One player will be human among the players.",
)
@click.option(
    "--impostors",
    required=False,
    default=1,
    type=int,
    help="Number of impostors in the game.",
)
def start(players, add_human, impostors):
    """Start the impostor game."""
    impostor_game = create_flow_impostor()
    initial_context = {
        "player_count": players,
        "add_human": add_human,
        "impostors": impostors,
    }
    impostor_game.run(initial_context)


if __name__ == "__main__":
    main()
