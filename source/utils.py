import arcade as arc

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
