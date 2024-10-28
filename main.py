import pygame
import sys
from game.game import Game
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, FPS

class LollmsPong:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("LollmsPong")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.game = None

    def draw_menu(self):
        self.screen.fill(BLACK)
        
        # Draw title
        title = self.font.render("LollmsPong", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        vs_text = self.font.render("1. VS Mode", True, WHITE)
        ai_text = self.font.render("2. AI Mode", True, WHITE)
        quit_text = self.font.render("3. Quit", True, WHITE)
        
        self.screen.blit(vs_text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))
        self.screen.blit(ai_text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2 + 80))
        self.screen.blit(quit_text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2 + 160))
        
        pygame.display.flip()

    def handle_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.start_game(vs_mode=True)
                    elif event.key == pygame.K_2:
                        self.start_game(vs_mode=False)
                    elif event.key == pygame.K_3:
                        self.quit_game()
            
            self.draw_menu()
            self.clock.tick(FPS)

    def start_game(self, vs_mode):
        self.game = Game()
        self.game.run()
        # After game ends, return to menu
        self.handle_menu()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.handle_menu()

def main():
    try:
        game = LollmsPong()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()