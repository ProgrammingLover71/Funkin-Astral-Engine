import arcade
import asset_manager

class Note(arcade.Sprite):
    def __init__(self, type, scale = 1, center_x = 0, center_y = 0, default_scroll: float = 1):
        super().__init__(asset_manager.manager.getNoteAsset(type), scale, center_x, center_y)
        self.scroll = default_scroll

    def setScrollSpeed(self, scroll_speed: float = 1):
        self.scroll = scroll_speed

    def update(self, dt: float = 1 / 60):
        self.center_y += 100 * self.scroll * dt