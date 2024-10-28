from typing import Tuple
import random
from game.constants import WINDOW_HEIGHT, PADDLE_HEIGHT, AI_DIFFICULTY_LEVELS

class AI:
    def __init__(self, difficulty: str = "MEDIUM"):
        """Initialize AI with specified difficulty level"""
        self.difficulty = difficulty
        self.reaction_delay = self._get_reaction_delay()
        self.prediction_accuracy = self._get_prediction_accuracy()
        self.frames_since_decision = 0
        self.target_y = WINDOW_HEIGHT // 2

    def _get_reaction_delay(self) -> int:
        """Get reaction delay based on difficulty"""
        delays = {
            "EASY": 30,
            "MEDIUM": 15,
            "HARD": 5
        }
        return delays.get(self.difficulty, 15)

    def _get_prediction_accuracy(self) -> float:
        """Get prediction accuracy based on difficulty"""
        accuracies = {
            "EASY": 0.6,
            "MEDIUM": 0.8,
            "HARD": 0.95
        }
        return accuracies.get(self.difficulty, 0.8)

    def calculate_move(self, paddle_y: float, ball_pos: Tuple[float, float], 
                      ball_speed: Tuple[float, float]) -> int:
        """
        Calculate the next move for the AI paddle
        Returns: 1 for up, -1 for down, 0 for no movement
        """
        self.frames_since_decision += 1
        
        # Only update decision after reaction delay
        if self.frames_since_decision < self.reaction_delay:
            return self._move_to_target(paddle_y)

        ball_x, ball_y = ball_pos
        speed_x, speed_y = ball_speed

        # Reset decision counter
        self.frames_since_decision = 0

        # Add randomness based on difficulty
        if random.random() > self.prediction_accuracy:
            self.target_y = ball_y + random.randint(-50, 50)
        else:
            # Predict ball position
            if speed_x > 0:  # Ball moving towards AI
                # Calculate approximate ball y position when it reaches paddle
                time_to_paddle = (WINDOW_HEIGHT - ball_x) / speed_x
                predicted_y = ball_y + (speed_y * time_to_paddle)
                
                # Keep prediction within screen bounds
                predicted_y = max(PADDLE_HEIGHT // 2, 
                                min(WINDOW_HEIGHT - PADDLE_HEIGHT // 2, predicted_y))
                
                self.target_y = predicted_y

        return self._move_to_target(paddle_y)

    def _move_to_target(self, paddle_y: float) -> int:
        """
        Determine movement direction to reach target Y position
        Returns: 1 for up, -1 for down, 0 for no movement
        """
        dead_zone = 10  # Pixels of tolerance
        if paddle_y + PADDLE_HEIGHT // 2 < self.target_y - dead_zone:
            return 1  # Move down
        elif paddle_y + PADDLE_HEIGHT // 2 > self.target_y + dead_zone:
            return -1  # Move up
        return 0  # Stay in position

    def update_difficulty(self, new_difficulty: str) -> None:
        """Update AI difficulty level"""
        if new_difficulty in AI_DIFFICULTY_LEVELS:
            self.difficulty = new_difficulty
            self.reaction_delay = self._get_reaction_delay()
            self.prediction_accuracy = self._get_prediction_accuracy()
            self.frames_since_decision = 0