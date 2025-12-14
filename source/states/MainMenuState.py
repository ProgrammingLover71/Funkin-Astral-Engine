# Friday Night Funkin' Astral Engine

### Main Menu Module
# This module defines the MainMenuState class, which represents the main menu.
# It appears after the title screen.

from AssetManager import *
from StateManager import *
from utils import draw_tex


class MainMenuState(State):
    def __init__(self, window: arc.Window):
        super().__init__(window, background_color = arc.color.BLACK)

    def setup(self):
        super().setup()
        
        self.menu_bg = AssetManager.load_image("mainMenu/background", "assets/images/MainMenu/menuBG.png").apply_brightness(0.8)
        # BUTTONSSS
        self.storymode_img = AssetManager.load_image("mainMenu/storyMode", "assets/images/MainMenu/storymode.png")
        self.freeplay_img  = AssetManager.load_image("mainMenu/freeplay", "assets/images/MainMenu/freeplay.png")
        self.options_img   = AssetManager.load_image("mainMenu/options", "assets/images/MainMenu/options.png")
    
    def on_draw(self):
        self.clear()

        draw_tex(self, self.menu_bg.texture, 0, 0)
    
    def on_key_press(self, key, mods):
        if key == arc.key.ESCAPE:
            StateManager.show_state("title")
