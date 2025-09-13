from pocketflow import Node
import random


class AssignRoles(Node):
    def prep(self, shared):
        return {
            "player_count": shared["player_count"],
        }

    def exec(self, data):
        # Generate players named from A to Z
        player_count = data["player_count"]
        players = []

        for i in range(player_count):
            players.append(
                {
                    "name": chr(65 + i).capitalize(),
                    "role": "crew",
                    "status": "alive",
                }
            )

        # Assign one impostor randomly
        impostor = random.randint(0, player_count - 1)
        players[impostor]["role"] = "impostor"

        return players

    def post(self, shared, _prep_res, exec_res):
        shared["players"] = exec_res
