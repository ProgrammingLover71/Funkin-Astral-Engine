# Friday Night Funkin' Astral Engine

### Title State Module
# This module defines the TitleState class, which represents the title screen of the game.
# It appears first when the game is launched.

from AssetManager import *
from StateManager import *
from utils import draw_tex
import math
import random


#========== Intro text utility ==========#
def get_random_intro_line() -> str:
    intro_text_asset = AssetManager.load_text_file("introText", "assets/introText.txt")
    intro_lines = intro_text_asset.content.splitlines()
    return random.choice(intro_lines)


class TitleState(State):
    def __init__(self, window: arc.Window):
        super().__init__(window, background_color = arc.color.BLACK)
        self.gf_animation_frame = 0
        self.logo_animation_frame = 0
        self.logo_animation_factor = 12 / 60    # 12 FPS animation but scaled to the beat (maybe?), at 60 FPS update rate (just as in V-Slice FNF)
        self.gf_animation_factor =   24 / 60    # 24 FPS animation but scaled to the beat (maybe?), at 60 FPS update rate (just as in V-Slice FNF)
        
        self.intro_line0, self.intro_line1 = get_random_intro_line().split('--')
        self.rendering = False   # Flag to check if the scene started rendering
        

    def setup(self):
        super().setup()

        self.flash_group = arc.SpriteList()
        self.ngl_group   = arc.SpriteList()

        # Load title screen assets
        self.title_music = AssetManager.load_sound("titleScreen/music", "assets/sounds/TitleMenu/freakyMenu.ogg")

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
        self.beat = -1
        self.song_bpm = 102
        self.secs_per_beat = 60 / self.song_bpm
        self.cool_text = ""     # Currently displayed intro text
        # Load the VCR font and then make the Text object
        self.vcr_font = AssetManager.load_font("VCR", "assets/fonts/vcr.ttf")
        self.cool_text_arc = arc.Text(
            text = "",
            x = 0,
            y = self.height / 2 + 60,
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
            center_x = self.width / 2 - 40,
            center_y = 160,
            angle = 0,
            visible = False
        )
        self.ngl_group.append(self.ng_logo)

        # Values for the flashbang
        self.flash_alpha = 255.0
        self.flash_img = AssetManager.load_image("titleScreen/flashbang", "assets/images/shared/flashbang.png")
        self.flash = arc.Sprite(self.flash_img.texture, center_x=self.width / 2, center_y=self.height / 2)          # Center the sprite (i'm an idiot and forgot to set the center)
        self.flash_group.append(self.flash)

        # Menu text
        self.menu_text = arc.Text(
            text = "Press [Enter] to Start",
            x = self.width / 2,
            y = 30,
            color = arc.color.WHITE,
            font_size = 32,
            anchor_x = "center",
            font_name = "VCR OSD Mono"
        )
        

    
    def beat_hit(self):
        def addText(text: str):
            self.cool_text += text + "\n"
        
        def clearText():
            self.cool_text = ""
        
        if self.beat == 1:
            addText("The")
        elif self.beat == 2:
            addText("Funkin Crew Inc.")
        
        elif self.beat == 3:
            addText("presents")
            addText("")
            addText("")
            addText("")
            addText("(Wind Rider too)")
        
        elif self.beat == 4:
            clearText()
        
        elif self.beat == 5:
            addText("In association")
        elif self.beat == 6:
            addText("with")
        elif self.beat == 7:
            addText("")
            addText("Newgrounds")
            self.ng_logo.visible = True
        
        elif self.beat == 8:
            clearText()
            self.ng_logo.visible = False
        
        elif self.beat == 9:
            addText(self.intro_line0)
        elif self.beat == 11:
            addText(self.intro_line1)
        elif self.beat == 12:
            clearText()
        
        elif self.beat == 13:
            addText("Friday")
        elif self.beat == 14:
            if self.intro_line0 == "trending":
                addText("Nigth")
            else:
                addText("Night")
        elif self.beat == 15:
            addText("Funkin")
            addText("")
            addText("")
            addText("")
            addText("thx for playing astral guyz :}")
        elif self.beat >= 16:
            self.menu_text.font_size = 34   # Enlarge the menu text a bit (just a little bit)
        
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

        # Increment animation frames by the animation factors (to effectively animate at desired FPS)
        self.gf_animation_frame   += self.gf_animation_factor
        self.logo_animation_frame += self.logo_animation_factor

        # Draw the main text
        self.menu_text.draw()
    

    def on_draw(self):
        self.clear()
        # On the first render, start playing the title music and do some other one-time shit
        if not self.rendering:
            self.rendering = True
            # Reset the text and timer because for some reason the lag at the start stacks the calls up (why the fk is there even lag when it starts)
            self.beat = 0
            self.intro_timer = 0
            self.cool_text_arc.text = ""
            self.flash_alpha = 1.0
            # Start the badass music
            arc.play_sound(self.title_music.sound, loop=True)
            return

        if self.beat >= 16:
            self.draw_main()
            self.flash_group.draw()
            self.flash.alpha -= 128 / 60 if self.flash_alpha > 0 else 0
        else:
            self.cool_text_arc.draw() # Draw the intro text because Arcade likes the draw() call here (fk this man)
        
        self.ngl_group.draw()
        

    def on_update(self, delta_time: float):
        self.intro_timer += delta_time
        self.menu_text.font_size -= (self.menu_text.font_size - 32) / 60
        if self.intro_timer >= self.secs_per_beat:
            self.intro_timer -= self.secs_per_beat
            self.beat += 1
            self.beat_hit()
        
    
    def on_key_press(self, key, mods):
        # Exit the game if we press escape
        if key == arc.key.ESCAPE:
            arc.exit()

        # Go to the next menu (the main menu) -- too bad it's not implemented yet XD
        if key == arc.key.ENTER:
            StateManager.show_state("mainMenu")
