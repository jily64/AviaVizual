import pygame, os, math, json
from dotenv import load_dotenv
from Modules import MAVLinkAdapter, Func, Touch, classes
from datetime import datetime, timezone

load_dotenv()

RESOURCES_PATH = os.getenv("RESOURCES_PATH")
WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))

class MainScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.mav = MAVLinkAdapter.Adapter()

        self.state = "main"

        self.save = {}

        self.default_pressure = app.data["ground_preasure"]

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
        self.heading_font = pygame.font.Font(None, 50)
        self.heading = 0

        self.indicate_heading = [(WIDTH//2, HEIGHT//3-135), (WIDTH//2, HEIGHT//3-50), 7]

        # Wings Indicator
        self.left_wing = [(WIDTH//4-100, HEIGHT//2), (WIDTH//4+75, HEIGHT//2), 10]
        self.right_wing = [(WIDTH-WIDTH//4-100, HEIGHT//2), (WIDTH-WIDTH//4+75, HEIGHT//2), 10]

        self.left_body = [(WIDTH//2-50, HEIGHT//2-25), (WIDTH//2, HEIGHT//2), 7]
        self.right_body = [(WIDTH//2+50, HEIGHT//2-25), (WIDTH//2, HEIGHT//2), 7]

        # Altitude Setup
        self.alt_font = pygame.font.Font(None, 50)
        self.alt = 0

        self.relative_alt_font = pygame.font.Font(None, 50)
        self.relative_alt = 0

        # Speed Setup
        self.horizon_speed_font = pygame.font.Font(None, 50)
        self.horizon_speed = 0

        # Vertical Speed Setup
        self.vertical_speed_font = pygame.font.Font(None, 50)
        self.vertical_speed = 0

        # Time Setup
        self.time_font = pygame.font.Font(None, 50)
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

        # Pressure Setup
        self.press_font = pygame.font.Font(None, 50)
        self.press_text = self.press_font.render("1013.25", True, (0, 0, 0))
        self.press_rect = None

        press_rect = self.press_text.get_rect(center=(WIDTH-100, HEIGHT-20))
        self.app.touchable.add_rect(id="pressure_change", obj=press_rect, group="main", listner=self.pressure_callback)

        # FPS Setup
        self.fps_font = pygame.font.Font(None, 50)


    def update(self):
        angle_data = self.mav.get_ratio()
        global_data = self.mav.get_global()

        delta_vert = round(-math.cos(angle_data.pitch), 2)

        self.time = datetime.now(timezone.utc).strftime("%H:%M:%S")

        self.heading = self.mav.get_current_heading()

        self.alt = global_data.alt / 1000.0
        self.relative_alt = global_data.relative_alt / 1000.0

        self.horizon_speed = Func.count_speed_module(global_data.vx,global_data.vy) / 1000
        self.vertical_speed = global_data.vz / 1000

        self.horizon_sprite_current = pygame.transform.rotate(self.horizon_sprite, angle_data.roll)
        self.horizon_rect = self.horizon_sprite_current.get_rect(center=(self.horizon_rect.center[0], HEIGHT//2+delta_vert*10))

        self.compass_sprite_current = pygame.transform.rotate(self.compass_sprite, self.heading)
        self.compass_rect = self.compass_sprite_current.get_rect(center=self.compass_rect.center)
        


    def render(self):
        heading_surface = self.heading_font.render(str(self.heading), True, (255, 255, 255))
        heading_text_rect = heading_surface.get_rect(center=(WIDTH//2, 20))

        time_surface = self.heading_font.render(str(round(self.app.clock.get_fps())) + " (UTC)", True, (255, 255, 255))
        time_text_rect = heading_surface.get_rect(center=(WIDTH//2, HEIGHT-20))

        pressure = round(self.mav.get_pressure(), 2)
        pressure = round(1013.25, 2)

        alt_surface = self.heading_font.render(str(Func.calculate_height_from_pressure(self.app, self.default_pressure, pressure)), True, (255, 255, 255))
        alt_text_rect = heading_surface.get_rect(center=(50, HEIGHT//2-20))

        press_surface = self.press_font.render(str(pressure) + " гПа", True, (255, 255, 255))
        press_rect = press_surface.get_rect(center=(WIDTH-100, HEIGHT-20))

        relative_alt_surface = self.heading_font.render(str(self.alt), True, (255, 255, 255))
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

        self.screen.blit(press_surface, press_rect)

        self.screen.blit(horizon_speed_surface, horizon_speed_rect)

        pygame.draw.line(self.screen, (235, 235, 0), self.indicate_heading[0], self.indicate_heading[1], self.indicate_heading[2])

        self.screen.blit(self.compass_sprite_current, self.compass_rect)

        pygame.draw.line(self.screen, (235, 0, 0), self.left_wing[0], self.left_wing[1], self.left_wing[2])
        pygame.draw.line(self.screen, (235, 0, 0), self.right_wing[0], self.right_wing[1], self.right_wing[2])

        pygame.draw.line(self.screen, (235, 0, 0), self.left_body[0], self.left_body[1], self.left_body[2])
        pygame.draw.line(self.screen, (235, 0, 0), self.right_body[0], self.right_body[1], self.right_body[2])

    def update_save(self):
        with open("save.json", "r", encoding="UTF-8") as f:
            self.save = json.load(f)


    def settings_callback(self):
        self.app.change_group("settings")
    
    def pressure_callback(self):
        self.app.groups["scale_keyboard"].setup_value(value=self.default_pressure, callback=self.pressure_scale_callback, step=0.25)
        self.app.change_group("scale_keyboard")

    def pressure_scale_callback(self, value):
        self.default_pressure = value
        self.app.data["ground_pressure"] = value
        self.app.update_save()

class HeadingPlanner:
    def __init__(self, app):
        self.app=app
        self.screen = app.screen
        self.zones = app.t_h.zones_count//2

        self.title_font = pygame.font.Font(None, 75)

        self.GREEN = (0, 230, 0)
        self.RED = (230, 0, 0)

        self.ACTIVE_COLOR = self.RED

        

        self.heading_buttons = []
        self.time_buttons = []

        self.texts = [[], []]

        self.texts = []
        self.main_font = pygame.font.Font(None, 75)

        self.padding = 50
        self.size = [400, 150]
        self.text_center = [self.size[0]//2, self.size[1]//2]


        self.now_used = [None, None]
        self.page = 0



        self.onoff_button = pygame.Rect(1300, self.padding, self.size[0], self.size[0])
        self.clear_button = pygame.Rect(1300, self.padding + 500, self.size[0], self.size[1]-50)
        self.back_button = pygame.Rect(1300, self.padding + 650, self.size[0], self.size[1]-50)
        self.page_swap = pygame.Rect(1300, self.padding + 850, self.size[0], self.size[1]-50)

        self.app.touchable.add_rect(id="hd-onoff", obj=self.onoff_button, group="head_menu", listner=self.set_active)
        self.app.touchable.add_rect(id="hd-back", obj=self.back_button, group="head_menu", listner=self.back_to_menu_callback)
        self.app.touchable.add_rect(id="hd-pageswap", obj=self.page_swap, group="head_menu", listner=self.page_swap_callback)


        self.callbacks = [[self.m1_c, self.m2_c, self.m3_c, self.m4_c, self.m5_c], [self.h1_c, self.h2_c, self.h3_c, self.h4_c, self.h5_c]]

        self.generate_buttons()

    def generate_buttons(self):
        for i in range(self.zones):
            pad_delt = (i + 1) * self.padding
            size_delt = i * self.size[1]
            self.heading_buttons.append(pygame.Rect(100 + self.padding + self.size[0], size_delt + pad_delt, self.size[0], self.size[1]))
            self.app.touchable.add_rect(id="hd-m-"+str(i+1), obj=self.heading_buttons[i], group="head_menu", listner=self.callbacks[0][i])

        
        for i in range(self.zones):
            pad_delt = (i + 1) * self.padding
            size_delt = i * self.size[1]
            self.time_buttons.append(pygame.Rect(100, size_delt + pad_delt, self.size[0], self.size[1]))
            self.app.touchable.add_rect(id="hd-h-"+str(i+1), obj=self.time_buttons[i], group="head_menu", listner=self.callbacks[1][i])




    def update(self):
        if self.app.t_h.is_active == True:
            self.ACTIVE_COLOR = self.GREEN
        else:
            self.ACTIVE_COLOR = self.RED

    def render(self):
        for i in range(len(self.heading_buttons)):
            pad_delt = (i + 1) * self.padding
            size_delt = i * self.size[1]

            pygame.draw.rect(self.screen, (200, 200, 200), self.heading_buttons[i])
            text_render = self.main_font.render(str(self.app.t_h.headings[i+5*self.page]), True, (255, 255, 255))
            self.screen.blit(text_render, text_render.get_rect(center=(100 + self.padding + self.size[0] + self.text_center[0], size_delt + pad_delt + self.text_center[1])))
        
        for i in range(len(self.time_buttons)):
            pad_delt = (i + 1) * self.padding
            size_delt = i * self.size[1]

            hours = round(self.app.t_h.zones[i+5*self.page].total_seconds() // 3600)
            minutes = round(self.app.t_h.zones[i+5*self.page].total_seconds() // 60)

            

            pygame.draw.rect(self.screen, (200, 200, 200), self.time_buttons[i])
            text_render = self.main_font.render(str(hours) + ":" + str(minutes), True, (255, 255, 255))
            self.screen.blit(text_render, text_render.get_rect(center=(100 + self.padding + self.text_center[0], size_delt + pad_delt + self.text_center[1])))
        
        pygame.draw.rect(self.screen, self.ACTIVE_COLOR, self.onoff_button)
        pygame.draw.rect(self.screen, (200, 200, 0), self.clear_button)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button)
        pygame.draw.rect(self.screen, (200, 200, 200), self.page_swap)

    def m1_c(self):
        print("m1")
    
    def m2_c(self):
        print("m2")

    def m3_c(self):
        print("m3")

    def m4_c(self):
        print("m4")

    def m5_c(self):
        print("m5")

    def h1_c(self):
        print("h1")
    
    def h2_c(self):
        print("h2")

    def h3_c(self):
        print("h3")

    def h4_c(self):
        print("h4")

    def h5_c(self):
        print("h5")

    def clear_callback(self):
        print("c1")

    def set_active(self):
        self.app.t_h.set_active()

    def clear_time_head(self):
        self.app.t_h.renew(self)

    def back_to_menu_callback(self):
        self.app.change_group("main")


    def start_stop(self):
        self.app.t_h.set_active()

    def page_swap_callback(self):
        self.page = 1 - (self.page%2)
        print(self.page)