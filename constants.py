# ── Piece types ──────────────────────
EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3

DIRECTIONS = [
    (-1, 0), # Up
    (1, 0),  # Down
    (0, -1), # Left
    (0, 1)   # Right
]

# ── Players ──────────────────────────────────────────────────
ATTACKER_PLAYER = "attacker"
DEFENDER_PLAYER = "defender"

# ── Board sizes ──────────────────────────────────────────────
BOARD_9 = 9
BOARD_11 = 11
DEFAULT_BOARD_SIZE = 11

# ── GUI ──────────────────────────────────────
CELL_SIZE = 62  # pixels per cell
BOARD_MARGIN = 36  # pixels around the grid
INFO_PANEL_WIDTH = 220  # right-side panel
FPS = 60
DELAY = 700 # 0.3 second
WINDOW_TITLE = "Hnefatafl — Viking Chess  ·   AI Project"

# ── Colors ────────────────────────────────────────
COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (181, 136, 99)
COLOR_THRONE = (255, 200, 50)
COLOR_CORNER = (80, 160, 80)
COLOR_GRID = (80, 50, 20)

COLOR_ATTACKER = (40, 40, 40)
COLOR_DEFENDER = (240, 240, 240)
COLOR_KING = (255, 190, 0)

COLOR_SELECTED = (50, 220, 80)
COLOR_VALID = (80, 160, 255)

# ── Difficulty depth map ──────────────────

DIFFICULTIES = {
    "Easy": 3,
    "Medium": 5,
    "Hard": 7
}
# ["Easy", "Medium", "Hard"]
ROLES        = {
    "Attacker": ATTACKER_PLAYER,
    "Defender": DEFENDER_PLAYER

}

POINTS_FOR_SURROUNDING = 8

POINTS_FOR_CORNER_DISTANCE = 5
