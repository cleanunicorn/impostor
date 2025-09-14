from pocketflow import Flow

from nodes.AssignRoles import AssignRoles
from nodes.CheckGameStatus import CheckGameStatus
from nodes.EndGame import EndGame
from nodes.ImpostorAction import ImpostorAction
from nodes.Discuss import Discuss
from nodes.Vote import Vote


def create_flow_impostor() -> Flow:
    """Create the impostor game flow."""

    assign_roles = AssignRoles()
    check_game_status = CheckGameStatus()
    impostor_action = ImpostorAction()
    discuss = Discuss()
    vote = Vote()
    end_game = EndGame()

    assign_roles >> check_game_status
    check_game_status - "impostor_wins" >> end_game
    check_game_status - "crew_wins" >> end_game
    check_game_status - "continue_game" >> impostor_action
    (
        impostor_action
        >> discuss
        >> vote
        # >> kill_player
        >> check_game_status
    )

    flow = Flow(start=assign_roles)

    return flow
