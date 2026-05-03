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
#  Board squares
C_LIGHT_SQ = (210, 185, 145)
C_DARK_SQ = (160, 120, 80)
C_GRID = (90, 60, 30)

#  Special squares
C_THRONE = (195, 155, 75)  # golden centre
C_CORNER = (55, 110, 55)  # green escape corners

#  Pieces
C_ATTACKER = (35, 35, 35)
C_ATTACKER_BORDER = (90, 90, 90)
C_DEFENDER = (235, 235, 215)
C_DEFENDER_BORDER = (160, 160, 140)
C_KING = (240, 195, 30)
C_KING_BORDER = (180, 135, 0)

#  Highlights
C_SELECTED = (50, 220, 80, 140)  # RGBA
C_VALID_MOVE = (60, 160, 255, 100)  # RGBA
C_LAST_MOVE = (255, 210, 50, 90)  # RGBA

#  UI chrome
C_BACKGROUND = (22, 22, 28)
C_PANEL_BG = (14, 14, 18)
C_TEXT = (220, 215, 200)
C_TEXT_DIM = (130, 120, 100)
C_ACCENT = (210, 165, 40)  # gold accent

# ── Difficulty depth map ──────────────────
DIFFICULTY_DEPTH = {
    "Easy": 1,
    "Medium": 3,
    "Hard": 5,
}
