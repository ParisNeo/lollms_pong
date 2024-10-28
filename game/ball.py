import pygame
import random
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, BALL_SIZE, BALL_SPEED, WHITE

class Ball:
    def __init__(self):
        """Initialize the ball with starting position and random direction"""
        self.size = BALL_SIZE
        self.reset()
        
    def reset(self):
        """Reset ball to center position with random direction"""
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        
        # Random angle between -45 and 45 degrees for initial direction
        angle = random.uniform(-45, 45)
        self.speed_x = BALL_SPEED * (1 if random.random() > 0.5 else -1)
        self.speed_y = random.uniform(-BALL_SPEED, BALL_SPEED)

    def move(self):
        """Update ball position and handle wall collisions"""
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Handle top and bottom wall collisions
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.size:
            self.speed_y *= -1
            
    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))
        
    def check_collision(self, paddle):
        """Check for collision with a paddle and handle bounce"""
        ball_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
        
        if ball_rect.colliderect(paddle_rect):
            # Reverse horizontal direction
            self.speed_x *= -1
            
            # Calculate relative collision position for varying bounce angle
            relative_intersect_y = (paddle.y + paddle.height/2) - (self.y + self.size/2)
            normalized_intersect = relative_intersect_y / (paddle.height/2)
            bounce_angle = normalized_intersect * 60  # Max 60 degree bounce
            
            # Adjust vertical speed based on collision point
            self.speed_y = -BALL_SPEED * math.sin(math.radians(bounce_angle))
            
            # Slightly increase speed after each paddle hit
            speed_multiplier = 1.1
            self.speed_x *= speed_multiplier
            self.speed_y *= speed_multiplier
            
            return True
            
        return False

    def is_out_of_bounds(self):
        """Check if ball has gone past paddles"""
        return self.x < 0 or self.x > WINDOW_WIDTH - self.size
        
    def get_position(self):
        """Return current ball position"""
        return (self.x, self.y)