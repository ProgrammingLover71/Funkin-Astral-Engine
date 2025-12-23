# Friday Night Funkin' Astral Engine

## State Manager
# The State Manager is used as a simpler way to manage the game's current state.
# A `State` is an Arcade `View` that features extra methods that facilitate switching via the manager.

import arcade as arc
import utils


###============ State Class ============###

class State(arc.View):
	"""
	Represents a game state.
	"""
	def __init__(self, window: arc.Window = None) -> None:
		super().__init__(window, background_color = arc.color.BLACK)
		self.loaded				= False
		self.substate: Substate = None

	# --- State managing ---

	def enter(self) -> None:
		"""Used when the state starts to get rendered."""
		self._world_camera = arc.Camera2D(position = (0, 0))
		self._world_camera.activate()

	def exit(self) -> None:
		"""Used when the state stops being rendered."""
		# Let the GC do its magic :)
		if self.substate: self.remove_substate()
		self._world_camera = None

	def setup(self) -> None:
		"""Used when the state loads for the first time."""
		pass

	# --- Substate managing (yes, each state does it) ---

	def set_substate(self, substate: "Substate") -> None:
		self.substate = substate
		self.substate.enter()
	
	def remove_substate(self) -> None:
		self.substate.exit()
		self.substate = None	# GC magic over here (again) :)

	# --- Main update/render logic ---

	def update(self, dt: float) -> None:
		"""Updates the internal state (or substate) logic. Do *not* override `on_update`!"""
		pass

	def draw(self) -> None:
		"""Renders the state (and substate, if it exists) to the screen. Do *not* override `on_draw`!"""
		pass

	# --- Conductor-related stuff ---

	def beat_hit(self) -> None:
		"""Runs when the Conductor reaches a new beat."""
		pass

	def step_hit(self) -> None:
		"""Runs when the Conductor reaches a new step."""
	
	# --- State/Substate logic (and Arcade) ---

	def on_update(self, dt: float) -> None:
		if self.substate:
			self.substate.update(dt)
		else:
			self.update(dt)
	
	def on_draw(self) -> None:
		self.draw()
		if self.substate:
			# Draw the substate on top, duhhh!
			self.substate.draw()



###============ Substate Class ============###

class Substate(State):
	"""
	Represents a substate. \n
	Substates are used when switching to an entirely different state is not necessary, such as when transitioning between menus or when pausing a song.
	"""
	def __init__(self, parent_state: State) -> None:
		self.parent = parent_state

	def enter(self) -> None:
		# Override `enter()` so we don't create another world camera
		pass

	def exit(self) -> None:
		# Same for `exit()`, we don't have any world camera to delete
		pass

	def update(self, dt: float) -> None:
		# Override `update()` because we have no substates (or sub-substates in this case) to handle
		pass

	def draw(self) -> None:
		# Do the same for `draw()`
		pass



###============ State Manager Class ============###

class StateManager:
	all_states: dict[str, State]	= {}
	substate_stack: list[Substate]	= []
	current_state: State         = None
	window: arc.Window           = None


	@classmethod
	def init(cls, win: arc.Window) -> None:
		"""
		Initializes the state manager.
		Args:
			`win` (arcade.Window): The main game window.
		"""
		cls.window = win


	@classmethod
	def register_state(cls, name: str, state: State) -> None:
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
	def show_state(cls, name) -> None:
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

		cls.current_state.enter()
		cls.window.show_view(cls.current_state)
		# We set its loaded state here so that it can actually run `on_show_view` with loaded=True 
		if not cls.current_state.loaded:
			cls.current_state.loaded = True   # so we don't set it up again

	
	###=============== TRANSITIONS ===============###


	class FadeTransition:
		FADE_IN  = "in"
		BLACK    = "black"
		FADE_OUT = "out"

		def __init__(
			self,
			window,
			target_state,
			fade_in: float = 0.2,
			black: float = 0.0,
			fade_out: float = 0.2,
		):
			self.window = window
			self.target_state = target_state

			self.fade_in = fade_in
			self.black = black
			self.fade_out = fade_out

			self.t_fade_in_end = fade_in
			self.t_black_end = fade_in + black
			self.t_fade_out_end = fade_in + black + fade_out

			self.elapsed = 0.0
			self.phase = self.FADE_IN
			self.switched = False
			self.finished = False

		def update(self, dt):
			self.elapsed += dt

			# Phase resolution (time-based, deterministic)
			if self.elapsed < self.t_fade_in_end:
				self.phase = self.FADE_IN

			elif self.elapsed < self.t_black_end:
				self.phase = self.BLACK
				if not self.switched:
					self.switched = True
					StateManager.show_state(self.target_state)

			elif self.elapsed < self.t_fade_out_end:
				self.phase = self.FADE_OUT

			else:
				self.finished = True

		def _alpha(self) -> int:
			if self.phase == self.FADE_IN:
				t = self.elapsed / self.fade_in
				return int(255 * utils.easeIn(min(t, 1)))

			if self.phase == self.BLACK:
				return 255

			if self.phase == self.FADE_OUT:
				t = (self.elapsed - self.t_black_end) / self.fade_out
				return int(255 * utils.easeOut(min(t, 1)))

			return 0

		def draw(self):
			arc.draw_rectangle_filled(
				self.window.width // 2,
				self.window.height // 2,
				self.window.width,
				self.window.height,
				(*arc.color.BLACK[:3], self._alpha())
			)

	