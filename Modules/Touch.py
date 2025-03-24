import pygame


RECTS = {
    "settings_button": None
}


class Touchable:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

    def add_rect(self, id, obj:pygame.Rect, group):
        if id not in RECTS:
            raise "Incorrect ID"
        if group not in self.app.groups:
            raise "Incorrect GroupID"


        pos_1 = (obj.centerx-obj.width//2, obj.centery-obj.height//2)
        pos_2 = (obj.centerx+obj.width//2, obj.centery+obj.height//2)

        RECTS[id] = [pos_1, pos_2, group]
    
    def update(self, mx, my):
        pass


    def settings_button(self):
        self.app.change_group("settings")