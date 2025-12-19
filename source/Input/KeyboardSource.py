from .InputStuff import *
from .Keybinds   import *

class KeyboardSource(InputSource):
	def __init__(self):
		self.pending = []

	def on_key_press(self, key, modifiers, time):
		# Check all Keybind actions
		for action, keys in Keybind.bindings.items():
			if key in keys:
				self.pending.append(InputEvent(self, time, action, InputEvent.Pressed))

	def on_key_release(self, key, modifiers, time):
		for action, keys in Keybind.bindings.items():
			if key in keys:
				self.pending.append(InputEvent(self, time, action, InputEvent.Released))
	
	def poll(self, current_time):
		events = self.pending
		self.pending = []
		return events