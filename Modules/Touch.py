import pygame


RECTS = {
    "settings_button": None
}


class Touchable:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

    def add_rect(self, id, obj:pygame.Rect, group, listner):
        if id not in RECTS:
            raise "Incorrect ID"

        pos_1 = (obj.centerx-obj.width//2, obj.centery-obj.height//2)
        pos_2 = (obj.centerx+obj.width//2, obj.centery+obj.height//2)

        RECTS[id] = [pos_1, pos_2, group, listner]

        print(RECTS)


    def update(self, x, y, button, pressed):
        if pressed:
            for obj in RECTS:
                print(obj)
                if x > RECTS[obj][0][0] and x < RECTS[obj][1][0]:
                    if y > RECTS[obj][0][1] and y < RECTS[obj][1][1]:
                        RECTS[obj][3]()

    def update_app(self, app):
        self.app = app

    def settings_button(self):
        self.app.change_group("settings")