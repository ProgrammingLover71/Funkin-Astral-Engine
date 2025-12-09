# Friday Night Funkin' Astral Engine
# Copyright (c) 2025 Wind Rider, All rights reserved.

### Main Module
# This is the main entry point for the Astral Engine application.

import arcade as arc
from states.TitleState import TitleState
from AssetManager import *

class Astral(arc.Window):
    def __init__(self):
        super().__init__(1280, 720, "Friday Night Funkin' - Astral Engine v0.1 (ALPHA BUILD)")
        self.asset_manager = AssetManager()
        self.title_state = TitleState(self.asset_manager, self)
        self.show_view(self.title_state)

    def on_draw(self):
        self.current_view.on_draw()

if __name__ == "__main__":
    print("Friday Night Funkin' - Astral Engine [Alpha Build]")
    print("Copyright (c) 2025 Wind Rider")
    app = Astral()
    print("ladies 'n' gentlemen its time fore some funkin' :P")
    arc.run()