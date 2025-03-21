import pygame, os
from dotenv import load_dotenv
from Modules import MAVLinkAdapter, Func

load_dotenv()

RESOURCES_PATH = os.getenv("RESOURCES_PATH")
WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))

class MainScreen:
    def __init__(self, screen):
        self.screen = screen

        self.horizon_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Background.png"), (WIDTH, HEIGHT*2.5))
        self.horizon_rect = self.horizon_sprite.get_rect()
        self.horizon_rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        self.ratio = Func.get_current_ratio()
        self.horizon_sprite = pygame.transform.rotate(self.horizon_sprite, self.ratio.roll)

    def render(self):
        self.screen.blit(self.horizon_sprite, self.horizon_rect)