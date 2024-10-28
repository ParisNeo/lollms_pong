import pygame
import random
import json
from enum import Enum
from typing import Tuple, List

# Initialize Pygame
pygame.init()

# Game Constants
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
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Paddle:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED
        self.score = 0

    def move(self, up: bool):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self):
        self.reset()
        self.rect = pygame.Rect(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, BALL_SIZE, BALL_SIZE)

    def reset(self):
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class AI:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.reaction_speed = 0.5
        elif difficulty == "medium":
            self.reaction_speed = 0.7
        else:
            self.reaction_speed = 0.9

    def move_paddle(self, paddle: Paddle, ball: Ball):
        if random.random() < self.reaction_speed:
            if paddle.rect.centery < ball.rect.centery:
                paddle.move(False)
            elif paddle.rect.centery > ball.rect.centery:
                paddle.move(True)

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        try:
            with open("leaderboard.txt", "r") as f:
                self.scores = json.load(f)
        except:
            self.scores = []

    def save_scores(self):
        with open("leaderboard.txt", "w") as f:
            json.dump(self.scores, f)

    def add_score(self, player_name: str, score: int):
        self.scores.append({"name": player_name, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]  # Keep only top 10
        self.save_scores()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LOLLMS Pong")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.font = pygame.font.Font(None, 36)
        
        self.player1 = Paddle(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, BLUE)
        self.player2 = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, 
                            WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, RED)
        self.ball = Ball()
        self.ai = None
        self.leaderboard = Leaderboard()
        self.vs_ai = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING:
            if keys[pygame.K_w]:
                self.player1.move(True)
            if keys[pygame.K_s]:
                self.player1.move(False)
                
            if not self.vs_ai:
                if keys[pygame.K_UP]:
                    self.player2.move(True)
                if keys[pygame.K_DOWN]:
                    self.player2.move(False)

    def update(self):
        if self.state == GameState.PLAYING:
            self.ball.move()
            
            # AI movement if enabled
            if self.vs_ai:
                self.ai.move_paddle(self.player2, self.ball)
            
            # Collision detection
            if self.ball.rect.colliderect(self.player1.rect) or \
               self.ball.rect.colliderect(self.player2.rect):
                self.ball.speed_x *= -1
            
            # Score detection
            if self.ball.rect.left <= 0:
                self.player2.score += 1
                self.ball.reset()
            elif self.ball.rect.right >= WINDOW_WIDTH:
                self.player1.score += 1
                self.ball.reset()
                
            # Check for game over
            if self.player1.score >= 10 or self.player2.score >= 10:
                self.state = GameState.GAME_OVER

    def render(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state == GameState.PLAYING:
            self.render_game()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
            
        pygame.display.flip()

    def render_menu(self):
        title = self.font.render("LOLLMS PONG", True, WHITE)
        vs_player = self.font.render("1. VS Player", True, WHITE)
        vs_ai = self.font.render("2. VS AI", True, WHITE)
        
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 200))
        self.screen.blit(vs_player, (WINDOW_WIDTH//2 - vs_player.get_width()//2, 300))
        self.screen.blit(vs_ai, (WINDOW_WIDTH//2 - vs_ai.get_width()//2, 350))

    def render_game(self):
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        score1 = self.font.render(str(self.player1.score), True, WHITE)
        score2 = self.font.render(str(self.player2.score), True, WHITE)
        self.screen.blit(score1, (WINDOW_WIDTH//4, 50))
        self.screen.blit(score2, (3*WINDOW_WIDTH//4, 50))

    def render_game_over(self):
        winner = "Player 1" if self.player1.score > self.player2.score else "Player 2"
        text = self.font.render(f"{winner} Wins!", True, WHITE)
        restart = self.font.render("Press SPACE to restart", True, WHITE)
        
        self.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250))
        self.screen.blit(restart, (WINDOW_WIDTH//2 - restart.get_width()//2, 350))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == GameState.MENU:
                        if event.key == pygame.K_1:
                            self.vs_ai = False
                            self.state = GameState.PLAYING
                        elif event.key == pygame.K_2:
                            self.vs_ai = True
                            self.ai = AI("medium")
                            self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER:
                        if event.key == pygame.K_SPACE:
                            self.__init__()

            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()