from pocketflow import Node
import random
from faker import Faker


def generate_player_names(count=None):
    fake = Faker()
    names = set()
    while len(names) < count:
        names.add(fake.first_name())
    return list(names)


class AssignRoles(Node):
    def prep(self, shared):
        return {
            "player_count": shared["player_count"],
        }

    def exec(self, data):
        player_count = data["player_count"]
        players = []

        available_names = generate_player_names(player_count)
        for i in range(player_count):
            players.append(
                {
                    "name": available_names[i],
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
