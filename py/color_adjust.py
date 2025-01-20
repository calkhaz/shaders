
ui = dict(
    saturation = dict(val = 1.2, min = 0.0,  max = 2.0),
    contrast   = dict(val = 1.0, min = 0.0,  max = 2.0),
    brightness = dict(val = 0.0, min = 0.0,  max = 2.0),
    hue        = dict(val = 0.0, min = 0.0,  max = 6.28318),
)


def build_nodes(ui: dict) -> dict[str, dict[str, float|int]]:
    nodes = dict(
        color_adjust = ui
    )

    return nodes

graph = 'input -> color_adjust -> output'
