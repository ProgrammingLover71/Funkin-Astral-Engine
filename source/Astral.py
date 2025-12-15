# Friday Night Funkin' Astral Engine

### Main Module
# This is the main entry point for Astral.

import arcade as arc
from states.TitleState import TitleState
from states.MainMenuState import MainMenuState
from AssetManager import *
from StateManager import *


class Astral(arc.Window):
    def __init__(self):
        super().__init__(1280, 720, "Friday Night Funkin' - Astral Engine v0.1 (Development Build)")
        # Set up the state manager
        StateManager.init(self)
        # Set up the game states
        self.title_state    = TitleState(self)
        self.mainMenu_state = MainMenuState(self)

        StateManager.register_state("title", self.title_state)
        StateManager.register_state("mainMenu", self.mainMenu_state)
        # Show the title state
        StateManager.show_state("title")

    def on_draw(self):
        self.current_view.on_draw()
    
    def on_key_press(self, symbol, modifiers):
        return self.current_view.key_press(symbol, modifiers)


if __name__ == "__main__":
    print("Friday Night Funkin' - Astral Engine 0.1 (Development Build)")
    print("Stirring some shit...")

    app = Astral()
    print("Ladies n gentlemen, it is time for some funkin'!")

    arc.run()