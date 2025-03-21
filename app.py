import pygame, sys, os, json
from Modules import Groups
from dotenv import load_dotenv


load_dotenv()
pygame.init()

WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))
FPS = int(os.getenv("SCREEN_FPS"))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avia Vizual 1.0")

clock = pygame.time.Clock()

groups = {
    "main": Groups.MainScreen(screen)
}

current_group = "main"

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        groups[current_group].render()
        
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()