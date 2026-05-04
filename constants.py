# ── Piece types (stored in board cells) ──────────────────────
EMPTY = 0
ATTACKER = 1
DEFENDER = 2
KING = 3

# ── Players ──────────────────────────────────────────────────
ATTACKER_PLAYER = "attacker"
DEFENDER_PLAYER = "defender"

# ── Board sizes ──────────────────────────────────────────────
BOARD_9 = 9
BOARD_11 = 11
DEFAULT_BOARD_SIZE = 11

# ── GUI — Cell & layout ──────────────────────────────────────
CELL_SIZE = 62  # pixels per cell
BOARD_MARGIN = 36  # pixels around the grid
INFO_PANEL_WIDTH = 220  # right-side panel
FPS = 60
WINDOW_TITLE = "Hnefatafl — Viking Chess  ·   AI Project"

# ── Colours (R, G, B) ────────────────────────────────────────
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
DIFFICULTY_DEPTH = {
    "Easy": 1,
    "Medium": 3,
    "Hard": 5,
}
