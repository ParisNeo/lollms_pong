import pygame
from game.constants import WINDOW_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, WHITE

class Paddle:
    def __init__(self, x: int, y: int, color: tuple = WHITE):
        """Initialize paddle with position and properties"""
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = color
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_up(self):
        """Move paddle up while keeping it within screen bounds"""
        if self.y > 0:
            self.y -= self.speed
            self.rect.y = self.y

    def move_down(self):
        """Move paddle down while keeping it within screen bounds"""
        if self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed
            self.rect.y = self.y

    def draw(self, screen: pygame.Surface):
        """Draw paddle on the screen"""
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        """Update paddle's rectangle position"""
        self.rect.x = self.x
        self.rect.y = self.y

    @property
    def position(self) -> tuple:
        """Get current paddle position"""
        return (self.x, self.y)

    @property
    def bounds(self) -> pygame.Rect:
        """Get paddle's bounding rectangle"""
        return self.rect