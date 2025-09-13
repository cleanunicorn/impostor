from pocketflow import Flow

from nodes.AssignRoles import AssignRoles
from nodes.CheckGameStatus import CheckGameStatus
from nodes.EndGame import EndGame
from nodes.ImpostorAction import ImpostorAction


def create_flow_impostor() -> Flow:
    """Create the impostor game flow."""

    assign_roles = AssignRoles()
    check_game_status = CheckGameStatus()
    # - crew wins
    # - impostor wins
    # - continue game
    impostor_action = ImpostorAction()
    # kill_player = KillPlayer()
    # discuss = Discuss()
    # vote = Vote()
    # kill voted player
    end_game = EndGame()

    assign_roles >> check_game_status
    check_game_status - "impostor_wins" >> end_game
    check_game_status - "crew_wins" >> end_game
    check_game_status - "continue_game" >> impostor_action
    (
        impostor_action
        # >> kill_player
        # >> discuss
        # >> vote
        # >> kill_player
        >> check_game_status
    )

    flow = Flow(start=assign_roles)

    return flow
