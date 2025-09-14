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
            "impostors": shared["impostors"],
            "add_human": shared["add_human"],
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
                    "type": "ai",
                }
            )

        # Assign impostors randomly
        for _ in range(data["impostors"]):
            while True:
                impostor = random.randint(0, player_count - 1)
                if players[impostor]["role"] != "impostor":
                    players[impostor]["role"] = "impostor"
                    break

        # Assign humans randomly
        if data["add_human"]:
            human = random.randint(0, player_count - 1)
            players[human]["type"] = "human"

        return players

    def post(self, shared, _prep_res, exec_res):
        shared["players"] = exec_res
