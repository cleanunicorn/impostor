from pocketflow import Node
from pydantic import BaseModel
from utils.call_llm import call_llm


class KillResponse(BaseModel):
    playerNameToKill: str


class ImpostorAction(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
        }

    def exec(self, data):
        # Human is player A
        print("It's the impostor's turn to act.")

        impostor_actions = []

        alive_crew = [
            p for p in data["players"] if p["role"] == "crew" and p["status"] == "alive"
        ]

        for key, p in enumerate(data["players"]):
            if p["status"] != "alive":
                continue
            if p["role"] != "impostor":
                continue

            #
            prompt = (
                """
                You are an impostor in a game similar to Mafia (party game). 
                Your goal is to eliminate all crew members without being caught. 
                You can only choose to kill one crew member per turn.

                Live crew members:
                """
                + ", ".join([c["name"] for c in alive_crew])
                + """
                Choose one crew member to kill from the list above.
            """
            )
            response = call_llm(
                prompt=prompt,
                model_output_type=KillResponse,
            )

            impostor_actions.append(
                {
                    "impostor": p["name"],
                    "kill": response.playerNameToKill,
                }
            )

        return impostor_actions

    def post(self, shared, _prep_res, impostor_actions):
        # Count the most voted player
        votes = {}
        for action in impostor_actions:
            player_to_kill = action["kill"]
            if player_to_kill not in votes:
                votes[player_to_kill] = 0
            votes[player_to_kill] += 1

        sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
        player_to_kill = sorted_votes[0][0]
        valid_players_to_kill = [
            p["name"]
            for p in shared["players"]
            if p["role"] == "crew" and p["status"] == "alive"
        ]

        if player_to_kill not in valid_players_to_kill:
            print(
                f"The impostor(s) tried to kill {player_to_kill}, but this player is not a valid target."
            )
            print(f"Valid targets are: {valid_players_to_kill}")
            print("No one was killed this turn.")
            return

        for p in shared["players"]:
            if p["name"] == player_to_kill:
                p["status"] = "dead"
                print(f"{p['name']} has been killed!")
                break
