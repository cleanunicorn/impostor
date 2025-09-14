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
            # Human
            if player["type"] == "human":
                print("==============================")
                print(
                    f"You are {player['name']} ({player['role']}). It's your turn to vote. Who do you think is the impostor?"
                )
                print("Alive players:")
                for idx, p in enumerate(alive_players):
                    print(f"{idx + 1}. {p['name']}")
                while True:
                    try:
                        choice = int(
                            input(
                                f"Enter the number of the player you want to vote for (1-{len(alive_players)}): "
                            )
                        )
                        if 1 <= choice <= len(alive_players):
                            voted_player = alive_players[choice - 1]["name"]
                            current_votes.append(
                                {
                                    "player": player["name"],
                                    "voted": voted_player,
                                }
                            )
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                continue

            # AI
            prompt = f"""
            You are {player["name"]} ({player["role"]}).
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
        sorted_votes = sorted(
            vote_count.items(), key=lambda item: item[1], reverse=True
        )
        if len(sorted_votes) > 1:
            if sorted_votes[0][1] == sorted_votes[1][1]:
                print("It's a tie! No player is killed this round.")
                return

        player_to_kill = sorted_votes[0][0]
        for p in shared["players"]:
            if p["name"] == player_to_kill:
                print(f"Player killed based on votes: {p['name']} ({p['role']})")
                p["status"] = "dead"
                break
