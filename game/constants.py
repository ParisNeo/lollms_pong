# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 15
BALL_SPEED = 7

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
FPS = 60
WINNING_SCORE = 10

# AI difficulty levels and their corresponding speeds and reaction times
AI_DIFFICULTY_LEVELS = {
    'EASY': {
        'speed': 5,
        'reaction_time': 0.3,
        'prediction_error': 0.3
    },
    'MEDIUM': {
        'speed': 6,
        'reaction_time': 0.2,
        'prediction_error': 0.2
    },
    'HARD': {
        'speed': 7,
        'reaction_time': 0.1,
        'prediction_error': 0.1
    }
}

# Text settings
FONT_SIZE = 36
SCORE_OFFSET = 30

# Game states
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"

# Input keys
KEY_UP1 = 'w'
KEY_DOWN1 = 's'
KEY_UP2 = 'up'
KEY_DOWN2 = 'down'
KEY_PAUSE = 'p'
KEY_QUIT = 'q'