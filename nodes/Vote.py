from pocketflow import Node
from pydantic import BaseModel
from utils.call_llm import call_llm


class VoteResponse(BaseModel):
    votedPlayerName: str


class Vote(Node):
    def prep(self, shared):
        return {
            "players": shared["players"],
            "discussion": shared.get("discussion", []),
        }

    def exec(self, data):
        players = data["players"]

        alive_players = [p for p in players if p["status"] == "alive"]

        print("Voting phase")
        print("------------")
        print(f"Alive players: {[p['name'] for p in alive_players]}")

        current_votes = []

        # Collect votes from each alive player
        for player in alive_players:
            prompt = f"""
            You are {player["name"]}.
            This is the discussion previous to the vote:
            """
            for d in data["discussion"]:
                prompt += f"{d['player']}: {d['message']}\n"

            prompt += (
                """
            You need to vote one player who you think is the impostor to kill.
            Alive players:
            """
                + ", ".join([p["name"] for p in alive_players])
                + """
            Choose one crew member to kill from the list above.
            """
            )

            vote_response = call_llm(
                prompt=prompt,
                model_output_type=VoteResponse,
            )
            current_votes.append(
                {
                    "player": player["name"],
                    "voted": vote_response.votedPlayerName,
                }
            )

            print(f"{player['name']} voted to kill {vote_response.votedPlayerName}")

        return current_votes

    def post(self, shared, _prep_res, player_votes):
        # Count votes and select the player with the most votes
        vote_count = {}
        for vote in player_votes:
            voted_player = vote["voted"]
            if voted_player not in vote_count:
                vote_count[voted_player] = 0
            vote_count[voted_player] += 1

        # Determine the player with the highest votes
        player_to_kill = max(vote_count, key=vote_count.get)
        for p in shared["players"]:
            if p["name"] == player_to_kill:
                print(f"Player killed based on votes: {p['name']} ({p['role']})")
                p["status"] = "dead"
                break
