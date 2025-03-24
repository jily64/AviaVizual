import pygame, os
from dotenv import load_dotenv

load_dotenv()


RESOURCES_PATH = os.getenv("RESOURCES_PATH")
WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))


class NumKeyBoard:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

        self.value = 10
        self.set_value = 1
        self.return_group = "main"
        self.mark = "Град"

        # Button Text Setup
        self.button_font = pygame.font.Font(size=500)

        # Value Text
        self.value_font = pygame.font.Font(size=100)
        self.value_text = None
        self.value_text_rect = None

    def update(self):
        pass

    def render(self):
        pass

class ScaleKeyBoard:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

        self.value = 1013.25
        self.set_value = 1
        self.return_group = "main"
        self.mark = "гПа"

        # Button Text Setup
        self.button_font = pygame.font.Font(size=500)

        # Value Text
        self.value_font = pygame.font.Font(size=100)
        self.value_text = None
        self.value_text_rect = None

        # + Button Setup
        self.plus_button_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Button.png"), (650, 650))
        self.plus_button_rect = self.plus_button_sprite.get_rect()
        self.plus_button_rect.center = (350, HEIGHT//2)
        
        self.plus_button_text = self.button_font.render("+", True, (255, 255, 255))
        self.plus_button_text_rect = self.plus_button_text.get_rect()
        self.plus_button_text_rect.center = (350, HEIGHT//2)

        self.app.touchable.add_rect(id="sk_plus", obj=self.plus_button_rect, group="scale_keyboard", listner=self.plus_callback)

        # - Button Setup
        self.minus_button_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Button.png"), (650, 650))
        self.minus_button_rect = self.minus_button_sprite.get_rect()
        self.minus_button_rect.center = (WIDTH-350, HEIGHT//2)

        self.minus_button_text = self.button_font.render("-", True, (255, 255, 255))
        self.minus_button_text_rect = self.minus_button_text.get_rect()
        self.minus_button_text_rect.center = (WIDTH-350, HEIGHT//2)

        self.app.touchable.add_rect(id="sk_minus", obj=self.minus_button_rect, group="scale_keyboard", listner=self.minus_callback)

        # Ready Button
        self.ready_button_text = self.value_font.render("Применить", True, (255, 255, 255))
        self.ready_button_text_rect = self.ready_button_text.get_rect()
        self.ready_button_text_rect.center = (WIDTH//2, HEIGHT//2+250)

        self.ready_button_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Button.png"), self.ready_button_text_rect.size)
        self.ready_button_rect = self.ready_button_sprite.get_rect()
        self.ready_button_rect.center = (WIDTH//2, HEIGHT//2+250)

        self.app.touchable.add_rect(id="sk_ready", obj=self.ready_button_rect, group="scale_keyboard", listner=self.ready_callback)


    def new_value(self, value, set_value=1, return_group="main", mark="гПа"):
        self.value = value
        self.set_value = set_value
        self.return_group = return_group
        self.mark = mark

    def update(self):
        self.value_text = self.value_font.render(str(self.value) + " " + self.mark, True, (255, 255, 255))
        self.value_text_rect = self.value_text.get_rect()
        self.value_text_rect.center = (WIDTH//2, HEIGHT//2-250)

    def render(self):

        self.screen.blit(self.plus_button_sprite, self.plus_button_rect)
        self.screen.blit(self.minus_button_sprite, self.minus_button_rect)
        self.screen.blit(self.ready_button_sprite, self.ready_button_rect)

        self.screen.blit(self.value_text, self.value_text_rect)

        self.screen.blit(self.minus_button_text, self.minus_button_text_rect)
        self.screen.blit(self.plus_button_text, self.plus_button_text_rect)
        self.screen.blit(self.ready_button_text, self.ready_button_text_rect)


    def plus_callback(self):
        self.value += self.set_value

    def minus_callback(self):
        self.value -= self.set_value

    def ready_callback(self):
        self.app.change_group(self.return_group)