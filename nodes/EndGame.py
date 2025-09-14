from pocketflow import Node


class EndGame(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
            "game_status": shared["game_status"],
        }

    def exec(self, data):
        print("Game Over!")
        if data["game_status"] == "crew_wins":
            print("Crew wins!")
            print(
                f"Live crew: {[p['name'] for p in data['players'] if p['role'] == 'crew' and p['status'] == 'alive']}"
            )
        elif data["game_status"] == "impostor_wins":
            print("Impostors win!")
            print(
                f"Live impostors: {[p['name'] for p in data['players'] if p['role'] == 'impostor' and p['status'] == 'alive']}"
            )
        else:
            print("???")

    def post(self, shared, _prep_res, _exec_res):
        pass
