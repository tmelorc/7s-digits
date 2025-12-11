APP_TITLE = "7-S Digits"
APP_AUTHOR = 'Thiago de Melo'
APP_VERSION = 3

display = []
vectors = {
    0: [1, 1, 1, 0, 1, 1, 1],
    1: [0, 0, 0, 0, 0, 1, 1],
    2: [0, 1, 1, 1, 1, 1, 0],
    3: [0, 0, 1, 1, 1, 1, 1],
    4: [1, 0, 0, 1, 0, 1, 1],
    5: [1, 0, 1, 1, 1, 0, 1],
    6: [1, 1, 1, 1, 1, 0, 1],
    7: [0, 0, 1, 0, 0, 1, 1],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 0, 1, 1, 1, 1, 1],
    '': [0, 0, 0, 0, 0, 0, 0]
}

segment_animation_order = [1, 2, 5, 7, 6, 3, 4]
segment_animation_speed = 30
initial_number_min = 3
initial_number_max = 999999
max_num_moviments = 20

# COLOR THEMES
ORANGE_THEME = ('#f9af46', '#36250f')
BLUE_THEME = ('#4d9aff', '#0e1e33')
GREEN_THEME = ('#0dff1a', '#023205')

ON_COLOR, OFF_COLOR = GREEN_THEME

HIGHLIGHT_COLOR = 'WHITE'
BACKGROUND_COLOR = "BLACK"
SEGMENT_OUTLINE_COLOR = BACKGROUND_COLOR


# CODE FOR DRAWING DIGITS - BE CAREFUL IF YOU CHANGE ANYTHING HERE!
digit_width = 200
digit_height = 250

segment_thickness = 24
segment_length = 80
segment_tail = segment_thickness / 2

origin = (digit_width // 2, digit_height // 2)
centers = [
    (origin[0] - segment_length//2 - segment_tail,
     origin[1] - segment_length//2 - segment_tail),
    (origin[0] - segment_length//2 - segment_tail,
     origin[1] + segment_length//2 + segment_tail),
    (origin[0],
     origin[1] - segment_thickness - segment_length),
    origin,
    (origin[0],
     origin[1] + segment_thickness + segment_length),
    (origin[0] + segment_length//2 + segment_tail,
     origin[1] - segment_length//2 - segment_tail),
    (origin[0] + segment_length//2 + segment_tail,
     origin[1] + segment_length//2 + segment_tail)
]


if __name__ == "__main__":
    None
