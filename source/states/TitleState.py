# Friday Night Funkin' Astral Engine
# Copyright (c) 2025 Wind Rider, All rights reserved.

### Title State Module
# This module defines the TitleState class, which represents the title screen of the game.
# It appears first when the game is launched, unless specified in the debug launch settings.

from AssetManager import *
from PIL import ImageEnhance
import math

#========== Drawing utility ==========#

def draw_tex(view: arc.View, texture: arc.Texture, x: float, y: float, angle: float = 0):
    arc.draw_texture_rect(
        texture, rect = arc.Rect.from_kwargs(
            x      = view.width / 2  + x,
            y      = view.height / 2 + y,
            width  = texture.width,
            height = texture.height
        ),  angle = angle
    )


#========== Intro text utility ==========#
def get_random_intro_line(asset_manager: AssetManager) -> str:
    intro_text_asset = asset_manager.load_text_file("introText", "assets/introText.txt")
    intro_lines = intro_text_asset.content.splitlines()
    import random
    return random.choice(intro_lines)


class TitleState(arc.View):
    def __init__(self, asset_manager: AssetManager, window: arc.Window):
        super().__init__(window, background_color=arc.color.BLACK)
        self.asset_manager = asset_manager
        self.gf_animation_frame = 0
        self.logo_animation_frame = 0
        self.logo_animation_factor = 6 / 60    # 6 FPS animation at 60 FPS update rate (just as in V-Slice FNF)
        self.gf_animation_factor = 12 / 60    # 12 FPS animation at 60 FPS update rate (just as in V-Slice FNF)
        
        self.intro_timer = 0.0
        self.intro_line0, self.intro_line1 = get_random_intro_line(self.asset_manager).split('--')

        self.rendering = False   # Flag to check if the scene started rendering
        self.start()
        

    def start(self):
        # Load title screen assets
        self.title_music = self.asset_manager.load_sound("mainMenu/music", "assets/sounds/TitleMenu/freakyMenu.ogg")

        self.title_image  = self.asset_manager.load_image("mainMenu/title", "assets/images/TitleMenu/logoBumpin.png")   # Title Logo
        self.gf_image     = self.asset_manager.load_image("mainMenu/gf",    "assets/images/TitleMenu/gfDanceTitle.png")  # Girlfriend on Speakers Image
        self.stage_images = [
            self.asset_manager.load_image(f"mainMenu/stage-back",     f"assets/images/shared/stageback.png").apply_brightness(0.4),
            self.asset_manager.load_image(f"mainMenu/stage-curtains", f"assets/images/shared/stagecurtains.png").apply_brightness(0.4),
            self.asset_manager.load_image(f"mainMenu/stage-front",    f"assets/images/shared/stagefront.png").apply_brightness(0.4),
        ]

        # Scale the assets so they're not too big
        self.title_image.apply_scale(0.8)
        self.gf_image.apply_scale(0.8)
        
        self.intro_timer = -4.5

    
    def draw_intro(self):
        x = 0
        y = self.height / 2 + 60

        text1 = [
            "The Funkin' Crew Inc.",
            "Presents",
            ""
        ]

        text2 = [
            "",
            "In association with...",
            "Newgrounds babyyyy"
        ]

        # Get a random line from the intro text list
        text3 = [
            self.intro_line0,
            self.intro_line1,
            ""
        ]

        text4 = [
            "Astral Engine by...",
            "",
            "Wind Rider (help me plz)"
        ]

        text5 = [
            "Friday Night",
            "Funkin'",
            "(the sexy ass game)"
        ]

        if self.intro_timer < 2.0:
            display_text = arc.Text('\n'.join(text1), x, y)
        elif self.intro_timer < 4.0:
            display_text = arc.Text('\n'.join(text2), x, y)
        elif self.intro_timer < 6.0:
            display_text = arc.Text('\n'.join(text3), x, y)
        elif self.intro_timer < 8.0:
            display_text = arc.Text('\n'.join(text4), x, y)
        elif self.intro_timer < 9.0:
            display_text = arc.Text('\n'.join(text5[:2]), x, y) # Hide the engine part for a bit
        elif self.intro_timer < 10.0:
            display_text = arc.Text('\n'.join(text5), x, y)
        else:
            return
        
        display_text.font_size = 48
        display_text.color = arc.color.WHITE
        display_text.width = 1280
        display_text.align = "center"
        display_text.multiline = True
        display_text.draw()


    def draw_main(self):
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
    
    def on_draw(self):
        self.clear()

        # On the first render, start playing the title music
        if not self.rendering:
            self.rendering = True
            arc.play_sound(self.title_music.sound, loop=True)

        if self.intro_timer < 10.0:
            self.draw_intro()
        else:
            self.draw_main()
        
    def on_update(self, delta_time: float):
        self.intro_timer += delta_time
        #print(self.intro_timer)
            
