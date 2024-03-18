color_adjust = dict(
    saturation = 1.0,
    contrast = 1.0,
    brightness = 0.0,
    hue_adjust = 0.0 # 2PI brings you back to 0.0
)

nodes = dict(
    color_adjust = color_adjust,
)

graph = 'input -> color_adjust -> output'
