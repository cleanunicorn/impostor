from pocketflow import Node
from pydantic import BaseModel, Field
from utils.call_llm import call_llm

class KillResponse(BaseModel):
    playerToKill: str = Field(..., description="Name of a live, non-impostor player to kill")

class ImpostorAction(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
        }

    def exec(self, data):
        # Human is player A
        print("It's the impostor's turn to act.")

        impostor_actions = []

        live_players = [p for p in data["players"] if p["status"] == "alive" if p["name"] != 'A']

        for key, p in enumerate(data["players"]):
            if p["role"] == "impostor" and p["status"] == "alive":
                if p['name'] == 'A': # Human player
                    print("Human impostor is taking action.")
                    while True:
                        print("Live players: ", [p['name'] for p in live_players if p['name'] != 'A'])
                        action = input("Who do you want to kill?").strip()
                        if action in [p['name'] for p in live_players]:
                            print(f"You have chosen to kill {action}.")
                            impostor_actions.append({
                                key: action
                            })
                        else:
                            print(f"Invalid player {action}. Please choose a valid player.")
                             # Here you can implement the action logic, e.g., killing a player
                else:
                    print("Impostor is taking action.")
                    prompt = f"""
                    You are an impostor in a social game.
                    You can see the following players: {', '.join([p['name'] for p in live_players])}.
                    You can choose to kill one of them.
                    Decide who to kill and respond with the name of the player you want to kill.
                    """
                    response = call_llm(prompt, model_output_type=KillResponse)

        pass

    def post(self, shared, _prep_res, exec_res):
        # shared["current_impostor"] = exec_res
        pass
