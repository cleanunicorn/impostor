from pocketflow import Node


class CheckGameStatus(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
        }

    def exec(self, data):
        players = data["players"]
        impostors = [
            p for p in players if p["role"] == "impostor" and p["status"] == "alive"
        ]
        crew = [p for p in players if p["role"] == "crew" and p["status"] == "alive"]

        print("=============================")
        print(f"Players: {[p['name'] for p in players if p['status'] == 'alive']}")

        if len(impostors) == 0:
            return "crew_wins"
        elif len(impostors) >= len(crew):
            return "impostor_wins"
        else:
            return "continue_game"

    def post(self, shared, _prep_res, exec_res):
        shared["game_status"] = exec_res
        return exec_res
