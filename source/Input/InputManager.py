# Friday Night Funkin' Astral Engine

### Input Manager module
# This module defines the input manager, a global tool used for efficiently centralizing and managing game input from multiple sources, such as:
#   - the keyboard
#   - a replay
#   - or any other valid source

from .InputStuff import *


#====== InputManager ======#

class InputManager:
	"""
	The main input handling class for the game. <br>
	Handles multiple sources and centralizes event handling.
	"""
	def __init__(self):
		self.sources: list[InputSource] = []
		self.queue: list[InputEvent]    = []
	

	def add_source(self, source: InputSource):
		self.sources.append(source)
	

	def update(self, current_time: float):
		for source in self.sources:
			self.queue.extend(source.poll(current_time))
	

	def poll(self):
		events = self.queue
		self.queue = []     # Clear the queue so we don't read events from past frames
		return events
