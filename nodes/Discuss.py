from pocketflow import Node
from pydantic import BaseModel
from utils.call_llm import call_llm


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

        print("Discussion phase:")
        print(f"Alive players: {[p['name'] for p in alive_players]}")

        current_discussion = []

        # Randomly sort players to simulate discussion order
        import random

        random.shuffle(alive_players)

        for p in alive_players:
            system_prompt = f"""
# Game Rules
**Mafia / Werewolf Rules (Short & Clear)**

* Players are secretly assigned roles: **Crew (villagers)** or **Impostors (mafia/werewolves)**.
* The game alternates between **Night** and **Day** phases.

  * **Night**: Impostors secretly choose one player to eliminate.
  * **Day**: All alive players discuss and **vote to eliminate** one player, suspecting them to be an impostor.
* Eliminated players reveal their roles and leave the game.
* **Win conditions**:

  * **Impostors win** if their number becomes **equal to or greater than** the number of crew.
  * **Crew wins** if **all impostors are eliminated**.

# Game Context
Phase **Day**.
Other alive players: {", ".join([pl["name"] for pl in alive_players if pl["name"] != p["name"]])}
                
            """

            if len(current_discussion) > 0:
                system_prompt += "# Ongoing discussion```\n"
            for d in current_discussion:
                system_prompt += f"{d['player']}: {d['message']}\n"

            system_prompt += f"""```\n
                You are {p['name']}, a player in a game similar to Mafia or Werewolf. 
            """

            # You are currently {'an **Impostor**' if p['role'] == 'impostor' else 'a **Crew member**'}. 
            # You will never reveal your role if you are an Impostor.

            response = call_llm(
                prompt="""
It is now daytime. Everyone wakes up.

Goal: 
Discuss and find who among you are the impostors.
Rules:
You may talk freely, share suspicions, defend yourself, or accuse others.
Try to reason based on behavior, previous votes, and patterns.
When discussion ends, you must vote to eliminate one player.
The player with the most votes will be eliminated and reveal their role.
After voting, the game will move to the night phase.

Reminder: 
If the number of impostors becomes equal to or greater than the number of crew, the impostors win. If all impostors are eliminated, the crew wins.
What do you say next? Keep it brief. Persuade others to benefit your role.
                """,
                system_prompt=system_prompt,
                model_output_type=DiscussionResponse,
            )

            print(system_prompt)
            print("-----")
            print(f"{p['name']} says:")
            print(response)

            current_discussion.append(
                {"player": p["name"], "message": response.message}
            )

        return current_discussion

    def post(self, shared, _prep_res, discussion):
        print(discussion)
        exit(0)
