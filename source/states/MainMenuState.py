# Friday Night Funkin' Astral Engine

### Main Menu Module
# This module defines the MainMenuState class, which represents the main menu.
# It appears after the title screen.

from AssetManager import *
from StateManager import *
from utils import draw_tex
from Keybinds import *
import math


class MainMenuState(State):
    def __init__(self, window: arc.Window):
        super().__init__(window, background_color = arc.color.BLACK)

    def setup(self):
        super().setup()
        
        self.menu_bg       = AssetManager.load_image("mainMenu/background", "assets/images/MainMenu/menuBG.png").apply_brightness(0.8)
        self.storymode_img = AssetManager.load_image("mainMenu/storyMode", "assets/images/MainMenu/storymode.png")
        self.freeplay_img  = AssetManager.load_image("mainMenu/freeplay",  "assets/images/MainMenu/freeplay.png")
        self.options_img   = AssetManager.load_image("mainMenu/options",   "assets/images/MainMenu/options.png")

        self.btn_texture_index = 0
        self.option_index      = 0
        
        # Camera stuff
        self.camera = arc.Camera2D()
        self.camera.position = arc.Vec2(0, 0)
        self.target_cam_y = 0

        # The actual buttons lol
        self.storymode_spr = arc.Sprite(self.storymode_img.texture[self.btn_texture_index], center_x = self.width / 2, center_y = self.height / 2 + 200)
        self.freeplay_spr  = arc.Sprite(self.freeplay_img.texture[self.btn_texture_index],  center_x = self.width / 2, center_y = self.height / 2 + 0)
        self.options_spr   = arc.Sprite(self.options_img.texture[self.btn_texture_index],   center_x = self.width / 2, center_y = self.height / 2 - 200)

        self.btn_sprites = arc.SpriteList()
        self.btn_sprites.append(self.storymode_spr)
        self.btn_sprites.append(self.freeplay_spr)
        self.btn_sprites.append(self.options_spr)
    

    def on_draw(self):
        self.clear()
        # Draw everything
        draw_tex(self, self.menu_bg.texture, 0, 0)
        self.btn_sprites.draw()
    

    def on_update(self, dt):
        self.btn_texture_index += 1 / 20
        self.btn_texture_index %= 4   # We have only 3 sprites for the idle animation

        cam_delta = (self.target_cam_y - self.camera.position.y) * 8 * dt

        # Move the camera (in 0.125s) -- I fucking hate immutable vectors bruh
        self.camera.position += arc.Vec2(0, cam_delta)

        # update the god damn sprites
        self.storymode_spr.center_y -= cam_delta
        self.freeplay_spr.center_y  -= cam_delta
        self.options_spr.center_y   -= cam_delta

        self.storymode_spr.texture = self.storymode_img.texture[math.floor(self.btn_texture_index)]
        self.freeplay_spr.texture  = self.freeplay_img.texture[math.floor(self.btn_texture_index)]
        self.options_spr.texture   = self.options_img.texture[math.floor(self.btn_texture_index)]
    

    def key_press(self, key, mods):
        if Keybinds.checkKeybind(key, Keybinds.Return):
            StateManager.show_state("title")
        
        if Keybinds.checkKeybind(key, Keybinds.Up):
            # Update the option only if we have what to set it to
            if self.option_index < 1:
                self.target_cam_y += 200
                self.option_index += 1

        if Keybinds.checkKeybind(key, Keybinds.Down):
            # Do the same here
            if self.option_index > -1:
                self.target_cam_y -= 200
                self.option_index -= 1
