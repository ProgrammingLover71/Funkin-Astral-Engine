# Friday Night Funkin' Astral Engine

### Input module
# This module defines the interface for any recognizible input source for the game, along with the interface for an input event.


#====== InputSource ======#

class InputSource:
    """
    Represents an input source for the game.

    <h2>Abstract Members:</h2>
    `poll(current_time: float)` - returns a list of all input events that have occured between the last poll and `current_time`.
    """
    def poll(self, current_time: float):
        return []


#====== InputEvent ======#

class InputEvent:
    """
    Represents an input event.
    """
    def __init__(self, src: InputSource, time: float, action: str, act_type: str):
        self.source   = src
        self.time     = time
        self.action   = action
        self.act_type = act_type

    Pressed  = "press"
    Released = "release"
