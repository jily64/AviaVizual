import pygame, sys, os, json, threading
from Modules import Groups, Touch, Keyboards, TimeHead
from dotenv import load_dotenv
from pynput import mouse

load_dotenv()

WIDTH, HEIGHT = int(os.getenv("SCREEN_WIDTH")), int(os.getenv("SCREEN_HEIGHT"))
FPS = int(os.getenv("SCREEN_FPS"))

class App:
    def __init__(self):
        pygame.init()

        self.running = True

        self.load_save()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Avia Vizual 1.0")

        self.clock = pygame.time.Clock()

        self.current_group = "main"

        self.touchable = Touch.Touchable(self)

        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

        self.t_h = TimeHead.TimeHead(self)

        self.groups = {
            "main": Groups.MainScreen(self),
            "head_menu": Groups.HeadingPlanner(self),
            "scale_keyboard": Keyboards.ScaleKeyBoard(self),
            "num_keyboard": Keyboards.NumKeyBoard(self)
        }

        self.touchable.update_app(self)
        
        

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.t_h.update()

            self.groups[self.current_group].update()

            self.screen.fill((0, 0, 0))

            self.groups[self.current_group].render()

            pygame.display.flip()

            self.clock.tick(60)


        pygame.quit()
        sys.exit()
        self.touchable.destroy()
        self.listener_thread.join()

    def start_listener(self):
        with mouse.Listener(on_click=self.touchable.update) as listener:
            listener.join()
    
    def change_group(self, id):
        if id not in self.groups:
            raise "Incorrect ID"
        
        self.current_group = id

    def ping(self):
        pass


    def load_save(self):
        with open("save.json", "r", encoding="UTF-8") as f:
            self.data = json.load(f)

    def update_save(self):
        with open("save.json", "w", encoding="UTF-8") as f:
            json.dump(self.data, f)

if __name__ == "__main__":
    app = App()
    app.run()