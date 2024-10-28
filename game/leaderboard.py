import json
import os
from typing import List, Dict
from datetime import datetime

class Leaderboard:
    def __init__(self, filename: str = "leaderboard.json"):
        """Initialize the leaderboard with a filename to store scores."""
        self.filename = filename
        self.scores: List[Dict] = []
        self.load_from_file()

    def add_score(self, player_name: str, score: int, game_mode: str) -> None:
        """Add a new score to the leaderboard."""
        score_entry = {
            "player_name": player_name,
            "score": score,
            "game_mode": game_mode,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scores.append(score_entry)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.save_to_file()

    def get_top_scores(self, limit: int = 10, game_mode: str = None) -> List[Dict]:
        """Get top scores, optionally filtered by game mode."""
        if game_mode:
            filtered_scores = [s for s in self.scores if s["game_mode"] == game_mode]
        else:
            filtered_scores = self.scores
        
        return filtered_scores[:limit]

    def save_to_file(self) -> None:
        """Save the current scores to a JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump({"scores": self.scores}, f, indent=4)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def load_from_file(self) -> None:
        """Load scores from the JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.scores = data.get("scores", [])
            else:
                self.scores = []
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            self.scores = []

    def clear_scores(self) -> None:
        """Clear all scores from the leaderboard."""
        self.scores = []
        self.save_to_file()

    def get_player_rank(self, player_name: str, game_mode: str = None) -> int:
        """Get the rank of a specific player, optionally filtered by game mode."""
        if game_mode:
            filtered_scores = [s for s in self.scores if s["game_mode"] == game_mode]
        else:
            filtered_scores = self.scores
        
        for i, score in enumerate(filtered_scores):
            if score["player_name"] == player_name:
                return i + 1
        return -1

    def get_high_score(self, game_mode: str = None) -> int:
        """Get the highest score, optionally filtered by game mode."""
        if not self.scores:
            return 0
            
        if game_mode:
            filtered_scores = [s for s in self.scores if s["game_mode"] == game_mode]
            return filtered_scores[0]["score"] if filtered_scores else 0
        
        return self.scores[0]["score"] if self.scores else 0