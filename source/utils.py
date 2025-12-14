import arcade as arc

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