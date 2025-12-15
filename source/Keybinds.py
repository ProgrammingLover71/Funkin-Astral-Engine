# Friday Night Funkin' Astral Engine

### Keybinds module
# This module defines the static class Keybinds, which stores (at runtime and locally) all the keybinds for the game.

import arcade as arc

class Keybinds:
    # Movement keybinds (default)
    Up    = [ arc.key.W, arc.key.UP ]
    Down  = [ arc.key.S, arc.key.DOWN ]
    Left  = [ arc.key.A, arc.key.LEFT ]
    Right = [ arc.key.D, arc.key.RIGHT ]
    # Some navigation keybinds
    Accept = [ arc.key.ENTER,  arc.key.X ]
    Return = [ arc.key.ESCAPE, arc.key.Z ]

    @staticmethod
    def checkKeybind(key, bind: list):
        for keybind in bind:
            if key == keybind: return True
        return False