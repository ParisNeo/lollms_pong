import pygame
import random
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 7
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

class GameMode(Enum):
    VS_PLAYER = 1
    VS_AI = 2

class AIDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

@dataclass
class Player:
    name: str
    score: int = 0
    color: Tuple[int, int, int] = WHITE

class Ball:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, BALL_SIZE, BALL_SIZE))

class Paddle:
    def __init__(self, x: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.color = color
        
    def move(self, up: bool):
        if up and self.y > 0:
            self.y -= PADDLE_SPEED
        elif not up and self.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.y += PADDLE_SPEED
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

class AI:
    def __init__(self, difficulty: AIDifficulty):
        self.difficulty = difficulty
        
    def move(self, paddle: Paddle, ball: Ball):
        reaction_speed = {
            AIDifficulty.EASY: 0.3,
            AIDifficulty.MEDIUM: 0.6,
            AIDifficulty.HARD: 0.9
        }[self.difficulty]
        
        if random.random() < reaction_speed:
            if ball.y > paddle.y + PADDLE_HEIGHT:
                paddle.move(False)
            elif ball.y < paddle.y:
                paddle.move(True)

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.load_scores()
        
    def load_scores(self):
        try:
            with open("leaderboard.json", "r") as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.scores = []
            
    def save_scores(self):
        with open("leaderboard.json", "w") as f:
            json.dump(self.scores, f)
            
    def add_score(self, player: Player):
        self.scores.append({"name": player.name, "score": player.score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]  # Keep top 10
        self.save_scores()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LOLLMS Pong")
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.ball = Ball()
        self.left_paddle = Paddle(50, random.choice(COLORS))
        self.right_paddle = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, random.choice(COLORS))
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.game_mode = None
        self.ai = None
        self.leaderboard = Leaderboard()
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Left paddle
        if keys[pygame.K_w]:
            self.left_paddle.move(True)
        if keys[pygame.K_s]:
            self.left_paddle.move(False)
            
        # Right paddle (if VS mode)
        if self.game_mode == GameMode.VS_PLAYER:
            if keys[pygame.K_UP]:
                self.right_paddle.move(True)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(False)
                
    def update(self):
        self.ball.move()
        
        # AI movement
        if self.game_mode == GameMode.VS_AI:
            self.ai.move(self.right_paddle, self.ball)
            
        # Ball collision with top/bottom
        if self.ball.y <= 0 or self.ball.y >= WINDOW_HEIGHT - BALL_SIZE:
            self.ball.dy *= -1
            
        # Ball collision with paddles
        if (self.ball.x <= self.left_paddle.x + PADDLE_WIDTH and 
            self.left_paddle.y <= self.ball.y <= self.left_paddle.y + PADDLE_HEIGHT):
            self.ball.dx *= -1
            
        if (self.ball.x + BALL_SIZE >= self.right_paddle.x and 
            self.right_paddle.y <= self.ball.y <= self.right_paddle.y + PADDLE_HEIGHT):
            self.ball.dx *= -1
            
        # Scoring
        if self.ball.x <= 0:
            self.player2.score += 1
            self.ball.reset()
        elif self.ball.x >= WINDOW_WIDTH:
            self.player1.score += 1
            self.ball.reset()
            
    def draw(self):
        self.screen.fill(BLACK)
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        
        # Draw scores
        font = pygame.font.Font(None, 74)
        score1 = font.render(str(self.player1.score), True, WHITE)
        score2 = font.render(str(self.player2.score), True, WHITE)
        self.screen.blit(score1, (WINDOW_WIDTH//4, 20))
        self.screen.blit(score2, (3*WINDOW_WIDTH//4, 20))
        
        pygame.display.flip()
        
    def show_menu(self):
        font = pygame.font.Font(None, 74)
        
        while True:
            self.screen.fill(BLACK)
            title = font.render("LOLLMS PONG", True, WHITE)
            vs_player = font.render("1. VS Player", True, WHITE)
            vs_ai = font.render("2. VS AI", True, WHITE)
            
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
            self.screen.blit(vs_player, (WINDOW_WIDTH//2 - vs_player.get_width()//2, 250))
            self.screen.blit(vs_ai, (WINDOW_WIDTH//2 - vs_ai.get_width()//2, 350))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_mode = GameMode.VS_PLAYER
                        return True
                    elif event.key == pygame.K_2:
                        self.game_mode = GameMode.VS_AI
                        self.ai = AI(AIDifficulty.MEDIUM)
                        return True
                        
    def run(self):
        running = self.show_menu()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
            # Check for game over (example: first to 5 points)
            if self.player1.score >= 5 or self.player2.score >= 5:
                winner = self.player1 if self.player1.score >= 5 else self.player2
                self.leaderboard.add_score(winner)
                running = False
                
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()