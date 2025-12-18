import arcade as arc
from math import sqrt

# draw_tex(), my love
def draw_tex(view: arc.View, texture: arc.Texture, x: float, y: float, angle: float = 0):
    arc.draw_texture_rect(
        texture, rect = arc.Rect.from_kwargs(
            x      = x,
            y      = y,
            width  = texture.width,
            height = texture.height
        ),  angle = angle
    )


#====== Math stuff ======#

def linearLerp(a, b, k):
    return a + (b - a) * k

def easeOut(t):
    # 1 - (1 - t)^2
    return 1 - (1 - t) ** 4

def easeIn(t):
    # t^2
    return t ** 4

def easeInOut(t):
    # x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2
    return 2 * (t ** 4) if t < 0.5 else 1 - (2 - 2 * t) ** 4 / 2
