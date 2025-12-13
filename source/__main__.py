# Friday Night Funkin' Astral Engine

### Main Module
# This is the main entry point for the Astral Engine application.

import arcade as arc
from states.TitleState import TitleState
from AssetManager import *

class Astral(arc.Window):
    def __init__(self):
        super().__init__(1280, 720, "Friday Night Funkin' - Astral Engine v0.1 (Alpha Build)")
        self.asset_manager = AssetManager()
        self.title_state = TitleState(self.asset_manager, self)
        self.show_view(self.title_state)
    
    def setup_view(self):
        self.current_view.setup()

    def on_draw(self):
        self.current_view.on_draw()
    
    def on_key_press(self, symbol, modifiers):
        return self.current_view.on_key_press(symbol, modifiers)


if __name__ == "__main__":
    print("Friday Night Funkin' - Astral Engine [Alpha Build]")
    print("hold up let it cook ;)")
    app = Astral()
    app.setup_view()
    print("ladies 'n' gentlemen its time for some funkin' :P")
    arc.run()