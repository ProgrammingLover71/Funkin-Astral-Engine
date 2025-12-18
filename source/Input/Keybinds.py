# Friday Night Funkin' Astral Engine

### Keybinds module
# This module defines the static class Keybinds, which stores (at runtime and locally) all the keybinds for the game.

import arcade as arc

class Keybind:
    Up    = "Up"
    Down  = "Down"
    Left  = "Left"
    Right = "Right"

    Accept = "Accept"
    Return = "Return"

    bindings = {
        Up:          [ arc.key.W,       arc.key.UP ],
        Down:        [ arc.key.S,       arc.key.DOWN ],
        Left:        [ arc.key.A,       arc.key.LEFT ],
        Right:       [ arc.key.D,       arc.key.RIGHT ],
        Accept:      [ arc.key.ENTER,   arc.key.X ],
        Return:      [ arc.key.ESCAPE,  arc.key.Z ]
    }

    @staticmethod
    def check(key, bind: str):
        for keybind in Keybind.bindings.get(bind, []):
            if key == keybind: return True
        return False