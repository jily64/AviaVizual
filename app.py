import pygame, sys, os, json
from Modules import Groups
from dotenv import load_dotenv
from pynput import mouse

load_dotenv()

WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))
FPS = int(os.getenv("SCREEN_FPS"))

class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Avia Vizual 1.0")

        self.clock = pygame.time.Clock()

        self.groups = {
            "main": Groups.MainScreen(self),
            "settings": Groups.SettingsScreen(self)
        }

        self.current_group = "main"

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.groups[self.current_group].update()

            self.screen.fill((0, 0, 0))

            self.groups[self.current_group].render()
            
            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
    
    def change_group(self, id):
        if id not in self.groups:
            raise "Incorrect ID"
        
        self.current_group = id

if __name__ == "__main__":
    app = App()
    app.run()