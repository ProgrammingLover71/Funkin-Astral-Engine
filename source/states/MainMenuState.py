# Friday Night Funkin' Astral Engine

### Main Menu State
# This module defines the MainMenuState class, which represents the main menu.
# It appears after the title screen.

from AssetManager import *
from StateManager import *
from Input import *
from utils import *
import math


class MainMenuState(State):
	def __init__(self, window: arc.Window, inp_mgr: InputManager):
		super().__init__(window)
		self.input_manager = inp_mgr

	def setup(self):
		super().setup()
		
		self.menu_bg       = AssetManager.load_image("mainMenu/background", "assets/images/MainMenu/menuBG.png").apply_brightness(0.8)
		self.storymode_img = AssetManager.load_image("mainMenu/storyMode", "assets/images/MainMenu/storymode.png")
		self.freeplay_img  = AssetManager.load_image("mainMenu/freeplay",  "assets/images/MainMenu/freeplay.png")
		self.options_img   = AssetManager.load_image("mainMenu/options",   "assets/images/MainMenu/options.png")

		self.btn_texture_index = 0
		self.option_index      = 0
		
		# Camera movement stuff
		self.target_cam_y = 0

		# The actual buttons lol
		self.storymode_spr = arc.Sprite(self.storymode_img.texture[self.btn_texture_index], center_x = 0, center_y = 200)
		self.freeplay_spr  = arc.Sprite(self.freeplay_img.texture[self.btn_texture_index],  center_x = 0, center_y = 0)
		self.options_spr   = arc.Sprite(self.options_img.texture[self.btn_texture_index],   center_x = 0, center_y = -200)

		self.btn_sprites = arc.SpriteList()
		self.btn_sprites.append(self.storymode_spr)
		self.btn_sprites.append(self.freeplay_spr)
		self.btn_sprites.append(self.options_spr)
	

	def draw(self):
		self.clear()
		self._world_camera.use()

		# Draw everything
		draw_tex(self.menu_bg.texture, 
				 self._world_camera.position.x,
				 self._world_camera.position.y)
		self.btn_sprites.draw()
	

	def update(self, dt):
		self.btn_texture_index += 1 / 20

		cam_delta = (self.target_cam_y - self._world_camera.position.y) * 8 * dt

		# Move the camera (in 0.125s) -- I fucking hate immutable vectors bruh
		self._world_camera.position += arc.Vec2(0, cam_delta)

		self.storymode_spr.texture = self.storymode_img.texture[math.floor(self.btn_texture_index) % 3]
		self.freeplay_spr.texture  = self.freeplay_img.texture[math.floor(self.btn_texture_index) % 3]
		self.options_spr.texture   = self.options_img.texture[math.floor(self.btn_texture_index) % 3]
	
		for event in self.input_manager.poll():
			if event.act_type == InputEvent.Pressed and event.action == Keybind.Return:
				StateManager.show_state("title")
			
			if event.act_type == InputEvent.Pressed and event.action == Keybind.Up:
				# Update the option only if we have what to set it to
				if self.option_index < 1:
					self.target_cam_y += 200
					self.option_index += 1
			
			if event.act_type == InputEvent.Pressed and event.action == Keybind.Down:
				# Do the same here
				if self.option_index > -1:
					self.target_cam_y -= 200
					self.option_index -= 1
