import pygame
from typing import Tuple, Optional
from .constants import *
from .paddle import Paddle
from .ball import Ball
from .ai import AI
from .leaderboard import Leaderboard

class Game:
    def __init__(self):
        # Initialize game components
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LollmsPong")
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.paddle1 = Paddle(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, BLUE)
        self.paddle2 = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, 
                            WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, RED)
        self.ball = Ball(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        
        # Game state
        self.score1 = 0
        self.score2 = 0
        self.game_mode = None  # 'VS' or 'AI'
        self.ai = AI()
        self.leaderboard = Leaderboard()
        self.paused = False
        self.game_over = False
        self.winner = None
        
        # Font setup
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        
        # Player 1 controls
        if keys[pygame.K_w]:
            self.paddle1.move_up()
        if keys[pygame.K_s]:
            self.paddle1.move_down()
            
        # Player 2 controls (only in VS mode)
        if self.game_mode == 'VS':
            if keys[pygame.K_UP]:
                self.paddle2.move_up()
            if keys[pygame.K_DOWN]:
                self.paddle2.move_down()

    def update(self) -> None:
        if self.paused or self.game_over:
            return

        self.ball.move()
        
        # AI movement in AI mode
        if self.game_mode == 'AI':
            self.ai.calculate_move(self.paddle2, self.ball)
            
        # Check collisions
        if self.ball.check_collision(self.paddle1) or \
           self.ball.check_collision(self.paddle2):
            self.ball.speed_x *= -1
            
        # Score points
        if self.ball.x <= 0:
            self.score2 += 1
            self.ball.reset()
        elif self.ball.x >= WINDOW_WIDTH:
            self.score1 += 1
            self.ball.reset()
            
        # Check win condition
        if self.score1 >= 10 or self.score2 >= 10:
            self.game_over = True
            self.winner = 1 if self.score1 >= 10 else 2
            self.leaderboard.add_score(f"Player {self.winner}", 
                                     max(self.score1, self.score2))

    def draw(self) -> None:
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw score
        score_surf1 = self.font.render(str(self.score1), True, WHITE)
        score_surf2 = self.font.render(str(self.score2), True, WHITE)
        self.screen.blit(score_surf1, (WINDOW_WIDTH//4, 20))
        self.screen.blit(score_surf2, (3*WINDOW_WIDTH//4, 20))
        
        # Draw center line
        pygame.draw.aaline(self.screen, WHITE, 
                          (WINDOW_WIDTH//2, 0), 
                          (WINDOW_WIDTH//2, WINDOW_HEIGHT))
        
        # Draw pause/game over message
        if self.paused:
            pause_surf = self.font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_surf, 
                           (WINDOW_WIDTH//2 - pause_surf.get_width()//2, 
                            WINDOW_HEIGHT//2))
        
        if self.game_over:
            game_over_surf = self.font.render(f"Player {self.winner} Wins!", 
                                            True, WHITE)
            self.screen.blit(game_over_surf, 
                           (WINDOW_WIDTH//2 - game_over_surf.get_width()//2, 
                            WINDOW_HEIGHT//2))
        
        pygame.display.flip()

    def set_mode(self, mode: str) -> None:
        """Set game mode to either 'VS' or 'AI'"""
        self.game_mode = mode
        self.reset_game()

    def reset_game(self) -> None:
        """Reset game state"""
        self.score1 = 0
        self.score2 = 0
        self.ball.reset()
        self.paddle1.y = WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2
        self.paddle2.y = WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2
        self.game_over = False
        self.winner = None

    def toggle_pause(self) -> None:
        """Toggle pause state"""
        self.paused = not self.paused

    def run(self) -> None:
        """Main game loop"""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()