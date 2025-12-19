# Friday Night Funkin' Astral Engine

## State Manager Module
# The State Manager is used as a simpler way to manage the game's current state.
# A `State` is an Arcade `View` that features extra methods that facilitate switching via the manager.

import arcade as arc


###============ State Class ============###

class State(arc.View):
	"""
	Represents a game state.
	"""
	loaded: bool = False

	def enter(self):
		"""Used when the state starts to get rendered."""
		self._world_camera = arc.Camera2D(position = (0, 0))
		self._world_camera.activate()

	def exit(self):
		"""Used when the state stops being rendered."""
		# Let the GC do its magic :)
		self._world_camera = None

	def setup(self):
		"""Used when the state loads for the first time."""
		pass

	def beat_hit(self):
		"""Runs when the Conductor reaches a new beat."""
		pass

	def step_hit(self):
		"""Runs when the Conductor reaches a new step."""



###============ State Manager Class ============###

class StateManager:
	all_states: dict[str, State] = {}
	current_state: State         = None
	window: arc.Window           = None

	@classmethod
	def init(cls, win: arc.Window):
		"""
		Initializes the state manager.
		Args:
			`win` (arcade.Window): The main game window.
		"""
		cls.window = win

	@classmethod
	def register_state(cls, name: str, state: State):
		"""
		Registers a game state to the internal state registry.
		Args:
			`name` (str): The name with which the state will be registered.
			`state` (State): The state to be registered.
		"""
		if cls.all_states.get(name) != None:
			return
		cls.all_states[name] = state
	
	@classmethod
	def show_state(cls, name):
		"""
		Shows a game state to the screen.
		Args:
			`name` (str): The name of the state to show.
		"""
		new_state = cls.all_states.get(name)
		if not new_state:
			return
		
		if cls.current_state != None:
			cls.current_state.exit()

		cls.current_state = new_state
		if not cls.current_state.loaded:
			cls.current_state.setup()
			cls.current_state.loaded = True   # so we don't set it up again

		cls.current_state.enter()
		cls.window.show_view(cls.current_state)
	