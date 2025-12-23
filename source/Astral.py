# Friday Night Funkin' Astral Engine

### Main
# This is the main entry point for Astral.

import arcade as arc
from states.TitleState import TitleState
from states.MainMenuState import MainMenuState
from AssetManager import *
from StateManager import *
from Input import *
from Conductor import Conductor


class Astral(arc.Window):
	def __init__(self):
		super().__init__(1280, 720, "Friday Night Funkin' - Astral Engine v0.1 (Development Build)")

		# Set up the state manager and all other managers
		StateManager.init(self)
		self.conductor	 = Conductor()
		self.inp_manager = InputManager()
		self.kb_source   = KeyboardSource()
		self.inp_manager.add_source(self.kb_source)
		self.main_time = 0
		self.song_time = 0
		self.current_time = 0

		# Set up the game states
		self.title_state    = TitleState(self, self.inp_manager, self.conductor)
		self.mainMenu_state = MainMenuState(self, self.inp_manager)

		StateManager.register_state("title", self.title_state)
		StateManager.register_state("mainMenu", self.mainMenu_state)
		# Show the title state
		StateManager.show_state("title")


	def on_draw(self):
		self.current_view.on_draw()
	
	def on_update(self, dt):
		self.main_time += dt
		self.current_time = self.main_time if StateManager.all_states.get("play", None) != StateManager.current_state else self.song_time
		self.inp_manager.update(self.current_time)   # you have no idea how streesd out i was bcz i forgot this god damn line
	
	def on_key_press(self, key, mods):
		# Delegate to the keyboard input source
		# Use `main_time` if we're not in PlayState (PS: it does not exist yet), otherwise use `song_time`
		self.kb_source.on_key_press(key, mods, self.current_time)
	
	def on_key_release(self, key, mods):
		# Delegate to the keyboard input source
		# Use `main_time` if we're not in PlayState (PS: it does not exist yet), otherwise use `song_time`
		self.kb_source.on_key_release(key, mods, self.current_time)


if __name__ == "__main__":
	print("Friday Night Funkin' - Astral Engine 0.1 (Development Build)")
	print("Stirring some shit...")

	app = Astral()
	print("Ladies n gentlemen, it is time for some funkin'!")

	arc.run()