# Friday Night Funkin' Astral Engine

### Title State Module
# This module defines the TitleState class, which represents the title screen of the game.
# It appears first when the game is launched.

from AssetManager import *
from StateManager import *
from Input import *
from utils import *
from Conductor import *
import math
import random


#========== Intro text utility ==========#
def get_random_intro_line() -> str:
	intro_text_asset = AssetManager.load_text_file("introText", "assets/introText.txt")
	intro_lines = intro_text_asset.content.splitlines()
	return random.choice(intro_lines)


class TitleState(State):

	#====== Config numbers ======#

	ANIMATION_FACTOR: float = 102 / 120     # Controls how fast the animations are (102/60 -> 4 times a measure, 102/120 -> 2 times a measure)
	FLASH_ALPHA_DECREASE: float = 128       # How much to decrease the flashbang's alpha by every second
	CONFIRM_COLOR_FRAME_NUMBER: int = 12    # How long a cycle lasts when changing the menu text color after pressing [Accept]
	MENU_TEXT_COL1: arc.color.Color = arc.color.WHITE    # The main color for the menu text
	MENU_TEXT_COL2: arc.color.Color = arc.color.YELLOW   # The secondary color for the menu text
	MENU_TEXT_SIZE: float = 34              # The size the menu text has by default
	MENU_TEXT_CONFIRM_SIZE: float = 40      # The size the menu text grows towards when pressing [Accept]
	CAM_CONFIRM_TARGET_ZOOM: float = 0.9    # The zoom towards which the camera eases when pressing [Accept]

	#====== Actual game logic ======#

	def __init__(self, window: arc.Window, inp_mgr: InputManager):
		super().__init__(window, background_color = arc.color.BLACK)
		self.gf_animation_frame   = 0
		self.logo_animation_frame = 0

		self.rendering = False
		self.intro_skipped = False

		self.input_manager = inp_mgr


	def setup(self):
		super().setup()

		self.intro_line0, self.intro_line1 = get_random_intro_line().split('--')
		
		# Stuff for the intro text animation
		self.accepted: bool   = False
		self.confirm_timer    = 0.0
		self.CONFIRM_DURATION = 4 * self.secs_per_beat      # = 4 beats in seconds
		self.confirm_text_frm = 0                           # We use this to determine the color of the main menu text

		self.flash_group = arc.SpriteList()
		self.ngl_group   = arc.SpriteList()

		# Load title screen assets
		self.title_music  = AssetManager.load_sound("titleScreen/music", "assets/sounds/TitleMenu/freakyMenu.ogg")
		self.title_image  = AssetManager.load_image("titleScreen/title", "assets/images/TitleMenu/logoBumpin.png")   # Title Logo
		self.gf_image     = AssetManager.load_image("titleScreen/gf",    "assets/images/TitleMenu/gfDanceTitle.png")  # Girlfriend on Speakers Image
		self.stage_images = [
			AssetManager.load_image(f"titleScreen/stage-back",     f"assets/images/shared/stageback.png").apply_brightness(0.4),
			AssetManager.load_image(f"titleScreen/stage-curtains", f"assets/images/shared/stagecurtains.png").apply_brightness(0.4),
			AssetManager.load_image(f"titleScreen/stage-front",    f"assets/images/shared/stagefront.png").apply_brightness(0.4),
		]

		# Scale the assets so they're not too big
		self.title_image.apply_scale(0.8)
		self.gf_image.apply_scale(0.8)
		
		# Intro shit (way too much WHY GOD WHY)
		self.intro_timer = 0
		self.beat = -1          # Set the beat to -1 to avoid showing the "The" intro text twice
		self.cool_text = ""     # Currently displayed intro text

		# Load the VCR font and then make the Text object
		self.vcr_font = AssetManager.load_font("VCR", "assets/fonts/vcr.ttf")
		self.cool_text_arc = arc.Text(
			text = "",
			x = -self.width / 2,
			y = 60,
			color = arc.color.WHITE,
			font_size = 28,
			align = "center",
			width = 1200,
			multiline = True,
			font_name="VCR OSD Mono"   # what a goofy ahh name
		)


		ng_logo_img = AssetManager.load_image("titleScreen/ng-logo", "assets/images/TitleMenu/newgrounds_logo.png").apply_scale(0.75)
		self.ng_logo = arc.Sprite(
			ng_logo_img.texture, 
			center_x = -40,     # Offset it a little to the left
			center_y = -200,
			angle = 0,
			visible = False
		)
		self.ngl_group.append(self.ng_logo)


		# Values for the flashbang
		self.flash_alpha = 255.0

		self.flash_img = AssetManager.load_image("titleScreen/flashbang", "assets/images/shared/flashbang.png")
		self.flash = arc.Sprite(self.flash_img.texture, center_x = 0, center_y = 0)

		self.flash_group.append(self.flash)


		# Menu text
		self.menu_text = arc.Text(
			text = f"Press [{Keybind.get_string_repr_for_bind('Accept')}] to Start",
			x = 0,
			y = -330,
			color = arc.color.WHITE,
			font_size = self.MENU_TEXT_SIZE,
			anchor_x = "center",
			font_name = "VCR OSD Mono"
		)

	
	def enter(self):
		super().enter()
		self.menu_text.font_size = self.MENU_TEXT_SIZE
		self.menu_text.color     = self.MENU_TEXT_COL1
		self._world_camera.zoom = 1

	
	def exit(self):
		self.accepted = False
		super().exit()
		

	def INTRO_addText(self, text: str):
		self.cool_text += text + "\n"
		
	def INTRO_clearText(self):
		self.cool_text = ""
	
	def beat_hit(self):
		
		if self.beat == 1:
			self.INTRO_addText("The")
		elif self.beat == 2:
			self.INTRO_addText("Funkin Crew Inc.")
		
		elif self.beat == 3:
			self.INTRO_addText("presents")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("(Wind Rider too)")
		
		elif self.beat == 4:
			self.INTRO_clearText()
		
		elif self.beat == 5:
			self.INTRO_addText("In association")
		elif self.beat == 6:
			self.INTRO_addText("with")
		elif self.beat == 7:
			self.INTRO_addText("")
			self.INTRO_addText("Newgrounds")
			self.ng_logo.visible = True
		
		elif self.beat == 8:
			self.INTRO_clearText()
			self.ng_logo.visible = False
		
		elif self.beat == 9:
			self.INTRO_addText(self.intro_line0)
		elif self.beat == 11:
			self.INTRO_addText(self.intro_line1)
		elif self.beat == 12:
			self.INTRO_clearText()
		
		elif self.beat == 13:
			self.INTRO_addText("Friday")
		elif self.beat == 14:
			if self.intro_line0 == "trending":
				self.INTRO_addText("Nigth")
			else:
				self.INTRO_addText("Night")
		elif self.beat == 15:
			self.INTRO_addText("Funkin")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("")
			self.INTRO_addText("(thx for playing astral)")
		elif self.beat >= 16:
			self.intro_skipped = True
			if not self.accepted: self.menu_text.font_size += 2
		
		self.cool_text_arc.text = self.cool_text
		


	def draw_main(self):
		# isn't the draw_tex helper lovely? :>
		# Draw the stage
		draw_tex(self, self.stage_images[0].texture, 0, -100)  # Back
		draw_tex(self, self.stage_images[1].texture, 0, -250)  # Curtains
		draw_tex(self, self.stage_images[2].texture, 0, -400)  # Front

		# Draw the girlfriend on speakers
		draw_tex(self, self.gf_image.texture[math.floor(self.gf_animation_frame) % 30], 0, -230)

		# Draw the logo
		draw_tex(self, self.title_image.texture[math.floor(self.logo_animation_frame) % 15], 0, 140)


		# Draw the main text
		self.menu_text.draw()
	

	def on_draw(self):
		self.clear()
		self._world_camera.use()

		# On the first render, start playing the title music and do some other one-time shit
		if not self.rendering:
			self.rendering = True
			# Reset the text and timer because for some reason the lag at the start stacks the calls up (why the fk is there even lag when it starts)
			self.beat = 0
			self.intro_timer = 0
			self.cool_text_arc.text = ""
			self.flash_alpha = 1.0
			# Start the badass music (override BPM to 102 just to be safe)
			Conductor.play_audio(self.title_music, bpm_override = 102)
			return

		if self.beat >= 16:
			self.draw_main()
			self.flash_group.draw()
			self.flash.alpha -= self.FLASH_ALPHA_DECREASE * (1 / 60) if self.flash_alpha > 0 else 0
		else:
			self.cool_text_arc.draw() # Draw the intro text because Arcade likes the draw() call here (fk this man)
			self.ngl_group.draw()

	
	##=============== UPDATE LOGIC ===============##


	def on_update(self, dt: float):
		# --- timer advancement ---
		self._advance_timers(dt)

		# --- animation stuff ---
		self._update_textures()

		# --- state & menu text handling ---
		if self.accepted:
			self._handle_confirm()
		else:
			self._decay_text_size()
		
		# --- update beats ---
		self._handle_beat(dt)

		# --- input polling ---
		self._handle_input()

	
	def _update_textures(self):
		# Increment animation frames by the animation factors (to effectively animate at desired FPS)
		self.gf_animation_frame   += self.ANIMATION_FACTOR
		self.logo_animation_frame += self.ANIMATION_FACTOR


	def _advance_timers(self):
		# Increment the intro and confirm text timers
		self.intro_timer += dt
		self.confirm_text_frm += 1


	def _handle_confirm(self):
		# Flash the menu text yellow
		if self.confirm_text_frm % self.CONFIRM_COLOR_FRAME_NUMBER >= (self.CONFIRM_COLOR_FRAME_NUMBER / 2):
			self.menu_text.color = self.MENU_TEXT_COL1
		else:
			self.menu_text.color = self.MENU_TEXT_COL2

		# Set the text size
		self.confirm_timer += dt
		t = min(self.confirm_timer / self.CONFIRM_DURATION, 1.0)
			
		self.menu_text.font_size = linearLerp(self.MENU_TEXT_SIZE, self.MENU_TEXT_CONFIRM_SIZE, easeOut(t))
		self._world_camera.zoom  = linearLerp(1.0, self.CAM_CONFIRM_TARGET_ZOOM, easeOut(t))
		
		if self.confirm_timer >= self.CONFIRM_DURATION:
			StateManager.show_state("mainMenu")
	
	def _decay_text_size(self):
		# Smooth the menu text back to its normal size
		self.menu_text.font_size -= (self.menu_text.font_size - self.MENU_TEXT_SIZE) * dt


	def _handle_beat(self, dt):
		# Check in with the Conductor
		beat_check, _ = Conductor.update(dt)
		if beat_check:
			self.beat_hit()
		

	def _handle_input(self):
		for event in self.input_manager.poll():
			if event.act_type == InputEvent.Pressed and event.action == Keybind.Return:
				arc.exit()
			
			if event.act_type == InputEvent.Pressed and event.action == Keybind.Accept:
				if not self.intro_skipped:
					self.intro_skipped = True
					self.beat = 16
				elif not self.accepted:
					self.playConfirm()
					self.accepted = True
					self.confirm_timer = 0.0
	

	def playConfirm(self):
		if self.accepted:
			return
		confirm_sound = AssetManager.load_sound("shared/menuConfirm", "assets/sounds/shared/confirmMenu.ogg")
		arc.play_sound(confirm_sound.sound)

