import pygame, os, math
from dotenv import load_dotenv
from Modules import MAVLinkAdapter, Func, Touch
from datetime import datetime, timezone

load_dotenv()

RESOURCES_PATH = os.getenv("RESOURCES_PATH")
WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))

class MainScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.mav = MAVLinkAdapter.Adapter()

        # Horizon Setup
        self.horizon_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Background.png"), (WIDTH*2, HEIGHT*2))
        self.horizon_rect = self.horizon_sprite.get_rect()
        self.horizon_rect.center = (WIDTH//2, HEIGHT//2)

        self.horizon_sprite = pygame.transform.rotate(self.horizon_sprite, 0)
        self.horizon_rect = self.horizon_sprite.get_rect(center=self.horizon_rect.center)

        self.horizon_sprite_current = self.horizon_sprite

        # Compass Setup
        self.compass_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Compass.png"), (WIDTH//3, WIDTH//3))
        self.compass_rect = self.compass_sprite.get_rect()
        self.compass_rect.center = (WIDTH//2, HEIGHT//2)

        self.compass_sprite = pygame.transform.rotate(self.compass_sprite, 0)
        self.compass_rect = self.compass_sprite.get_rect(center=self.compass_rect.center)

        self.compass_sprite_current = self.compass_sprite

        # Heading Setup
        self.heading_font = pygame.font.Font(size=50)
        self.heading = 0

        self.indicate_heading = [(WIDTH//2, HEIGHT//3-135), (WIDTH//2, HEIGHT//3-50), 7]

        # Wings Indicator
        self.left_wing = [(WIDTH//4-100, HEIGHT//2), (WIDTH//4+75, HEIGHT//2), 10]
        self.right_wing = [(WIDTH-WIDTH//4-100, HEIGHT//2), (WIDTH-WIDTH//4+75, HEIGHT//2), 10]

        self.left_body = [(WIDTH//2-50, HEIGHT//2-25), (WIDTH//2, HEIGHT//2), 7]
        self.right_body = [(WIDTH//2+50, HEIGHT//2-25), (WIDTH//2, HEIGHT//2), 7]

        # Altitude Setup
        self.alt_font = pygame.font.Font(size=50)
        self.alt = 0

        self.relative_alt_font = pygame.font.Font(size=50)
        self.relative_alt = 0

        # Speed Setup
        self.horizon_speed_font = pygame.font.Font(size=50)
        self.horizon_speed = 0

        # Vertical Speed Setup
        self.vertical_speed_font = pygame.font.Font(size=50)
        self.vertical_speed = 0

        # Time Setup
        self.time_font = pygame.font.Font(size=50)
        self.time = datetime.now(timezone.utc).strftime("%H:%M:%S")

        # Settings Setup
        self.settings_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Settings.png"), (100, 100))
        self.settings_rect = self.settings_sprite.get_rect()
        self.settings_rect.center = (75, 75)

        self.app.touchable.add_rect(id="settings_button", obj=self.settings_rect, group="main", listner=self.settings_callback)

        # Menu Setup
        self.menu_sprite = pygame.transform.scale(pygame.image.load(RESOURCES_PATH + "Menu.png"), (100, 100))
        self.menu_rect = self.menu_sprite.get_rect()
        self.menu_rect.center = (WIDTH-75, 75)


    def update(self):
        angle_data = self.mav.get_ratio()
        global_data = self.mav.get_global()

        delta_vert = round(math.cos(angle_data.pitch), 2)

        self.time = datetime.now(timezone.utc).strftime("%H:%M:%S")

        self.heading = self.mav.get_current_heading()

        self.alt = global_data.alt / 1000.0
        self.relative_alt = global_data.relative_alt / 1000.0

        self.horizon_speed = Func.count_speed_module(global_data.vx, global_data.vy) / 1000
        self.vertical_speed = global_data.vz

        self.horizon_sprite_current = pygame.transform.rotate(self.horizon_sprite, self.mav.get_ratio().roll)
        self.horizon_rect = self.horizon_sprite_current.get_rect(center=(self.horizon_rect.center[0], HEIGHT//2+delta_vert*10))

        self.compass_sprite_current = pygame.transform.rotate(self.compass_sprite, self.heading)
        self.compass_rect = self.compass_sprite_current.get_rect(center=self.compass_rect.center)
        

    def render(self):
        heading_surface = self.heading_font.render(str(self.heading), True, (255, 255, 255))
        heading_text_rect = heading_surface.get_rect(center=(WIDTH//2, 20))

        time_surface = self.heading_font.render(str(self.time) + " (UTC)", True, (255, 255, 255))
        time_text_rect = heading_surface.get_rect(center=(WIDTH//2, HEIGHT-20))

        alt_surface = self.heading_font.render(str(self.alt), True, (255, 255, 255))
        alt_text_rect = heading_surface.get_rect(center=(50, HEIGHT//2-20))

        relative_alt_surface = self.heading_font.render(str(self.relative_alt), True, (255, 255, 255))
        relative_alt_text_rect = heading_surface.get_rect(center=(50, HEIGHT//2+20))

        horizon_speed_surface = self.heading_font.render("HorzS " + str(self.horizon_speed), True, (255, 255, 255))
        horizon_speed_rect = horizon_speed_surface.get_rect(center=(WIDTH-100, HEIGHT//2+20))

        vertical_speed_surface = self.heading_font.render("VertS " + str(self.vertical_speed), True, (255, 255, 255))
        vertical_speed_rect = horizon_speed_surface.get_rect(center=(WIDTH-100, HEIGHT//2-20))

        self.screen.blit(self.horizon_sprite_current, self.horizon_rect)

        self.screen.blit(self.settings_sprite, self.settings_rect)
        self.screen.blit(self.menu_sprite, self.menu_rect)

        self.screen.blit(heading_surface, heading_text_rect)

        self.screen.blit(time_surface, time_text_rect)

        self.screen.blit(vertical_speed_surface, vertical_speed_rect)

        self.screen.blit(alt_surface, alt_text_rect)
        self.screen.blit(relative_alt_surface, relative_alt_text_rect)

        self.screen.blit(horizon_speed_surface, horizon_speed_rect)

        pygame.draw.line(self.screen, (235, 235, 0), self.indicate_heading[0], self.indicate_heading[1], self.indicate_heading[2])

        self.screen.blit(self.compass_sprite_current, self.compass_rect)

        pygame.draw.line(self.screen, (235, 0, 0), self.left_wing[0], self.left_wing[1], self.left_wing[2])
        pygame.draw.line(self.screen, (235, 0, 0), self.right_wing[0], self.right_wing[1], self.right_wing[2])

        pygame.draw.line(self.screen, (235, 0, 0), self.left_body[0], self.left_body[1], self.left_body[2])
        pygame.draw.line(self.screen, (235, 0, 0), self.right_body[0], self.right_body[1], self.right_body[2])


    def settings_callback(self):
        self.app.change_group("settings")

class SettingsScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

        self.title_font = pygame.font.Font(size=75)

    def update(self):
        pass

    def render(self):
        title_text = self.title_font.render("Settings",True, (255, 255, 255))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (WIDTH//2, 50)

        self.screen.blit(title_text, title_text_rect)
        

        
