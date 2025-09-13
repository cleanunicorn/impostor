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
    default=4,
    type=int,
    help="Number of players in the game (default: 4).",
)
def start(players):
    """Start the impostor game."""
    impostor_game = create_flow_impostor()
    initial_context = {
        "player_count": players,
    }
    impostor_game.run(initial_context)


if __name__ == "__main__":
    main()
