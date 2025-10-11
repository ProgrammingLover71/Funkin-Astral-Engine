import arcade
import notes
import asset_manager

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"


class Player(arcade.Sprite):
    def update(self, delta_time = 1 / 60):
        pass


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = None
        self.player_sprite = None

        self.background_color = arcade.color.BLACK
    
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.note_list = arcade.SpriteList()
        self.player_sprite = Player(asset_manager.manager.getPlayerAsset(), scale = arcade.Vec2(1, 1.5))
        self.player_sprite.center_x = 950
        self.player_sprite.center_y = 250

        self.player_list.append(self.player_sprite)
        self.note_list.append(notes.Note("up", scale = arcade.Vec2(1, 1), default_scroll = 1))
    
    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.note_list.draw()
    
    def on_update(self, dt):
        self.player_list.update(dt)
        self.note_list.update(dt)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.E: print("LEFT")
        if key == arcade.key.R: print("UP")
        if key == arcade.key.I: print("DOWN")
        if key == arcade.key.O: print("RIGHT")

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()