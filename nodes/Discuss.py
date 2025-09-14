from pocketflow import Node
from pydantic import BaseModel
from utils.call_llm import call_llm
from textwrap import dedent


class DiscussionResponse(BaseModel):
    message: str


class Discuss(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
        }

    def exec(self, data):
        players = data["players"]
        alive_players = [p for p in players if p["status"] == "alive"]

        print("Discussion phase")
        print("----------------")
        print(f"Alive players: {[p['name'] for p in alive_players]}")

        current_discussion = []

        # Randomly sort players to simulate discussion order
        import random

        random.shuffle(alive_players)

        for p in alive_players:
            # Human
            if p["type"] == "human":
                print("==============================")
                print(
                    f"You are {p['name']} ({p['role']}). It's your turn to speak in the discussion. What do you say?"
                )
                message = input("Your message: ")
                current_discussion.append({"player": p["name"], "message": message})
                continue

            # AI
            system_prompt = dedent(f"""
                Act like you are a player in a party game very similar to Mafia (also known as Werewolf).  
                Your objective is to fully immerse yourself in the game role, simulate the thought process of a real player, and act accordingly. Be vivid, strategic, and dynamic in your reasoning.  
                Keep your role hidden unless strategically beneficial.  
                Justify your suspicions and decisions with clear reasoning, mimicking real human deduction and bluffing.  
            """)

            response = call_llm(
                system_prompt=system_prompt,
                prompt=f"""
                    You are {p["name"]}, your role is {"impostor" if p["role"] == "impostor" else "crew"}.
                    You may talk freely, share suspicions, defend yourself, or accuse others.
                    All players alive: {", ".join([pl["name"] for pl in alive_players if pl["name"] != p["name"]])}.
                    Convince the other players of your innocence if you are crew, or deflect suspicion if you are the impostor.
                    Here is what has been said so far in the discussion:\n```"""
                + (
                    "\n".join(
                        [f"{d['player']}: {d['message']}" for d in current_discussion]
                    )
                    if current_discussion
                    else " No one has spoken yet."
                )
                + """\n```
                    What do you say next to influence the discussion? Be brief and to the point.
                """,
                model_output_type=DiscussionResponse,
            )

            print(f"{p['name']} says:")
            print(response.message)

            current_discussion.append(
                {"player": p["name"], "message": response.message}
            )

        return current_discussion

    def post(self, shared, _prep_res, discussion):
        shared["discussion"] = discussion
