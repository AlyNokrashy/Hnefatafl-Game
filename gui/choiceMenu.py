import pygame
import sys
from constants import DIFFICULTIES, ROLES

BG_COLOR     = (30, 25, 20)
TEXT_COLOR   = (220, 210, 190)
DIM_COLOR    = (120, 110, 90)
ACCENT       = (210, 165, 40)
HOVER_COLOR  = (60, 50, 35)
SELECT_COLOR = (80, 65, 30)


import pygame
import sys
from constants import DIFFICULTIES, ROLES

BG_COLOR     = (30, 25, 20)
TEXT_COLOR   = (220, 210, 190)
DIM_COLOR    = (120, 110, 90)
ACCENT       = (210, 165, 40)
HOVER_COLOR  = (60, 50, 35)
SELECT_COLOR = (80, 65, 30)


import pygame
import sys
from constants import DIFFICULTIES, ROLES

BG_COLOR     = (30, 25, 20)
TEXT_COLOR   = (220, 210, 190)
DIM_COLOR    = (120, 110, 90)
ACCENT       = (210, 165, 40)
HOVER_COLOR  = (60, 50, 35)
SELECT_COLOR = (80, 65, 30)


def run_menu(screen) -> tuple[str, str, str, int]:
    """Blocks until the user confirms.
    Returns (mode, role, difficulty, board_size).
    - mode: 'Human vs AI' or 'Human vs Human'
    - role: 'Attacker' or 'Defender'  (always active)
    - difficulty: 'Easy' / 'Medium' / 'Hard'  (only active in Human vs AI)
    - board_size: 9 or 11
    """
    font_title = pygame.font.SysFont("Segoe UI", 40, bold=True)
    font_head  = pygame.font.SysFont("Segoe UI", 25, bold=True)
    font_btn   = pygame.font.SysFont("Segoe UI", 17)
    font_hint  = pygame.font.SysFont("Segoe UI", 17)

    # Defaults
    selected_mode       = "Human vs AI"
    selected_role       = "Attacker"
    selected_difficulty = "Medium"
    selected_board_size = 11

    modes = ["Human vs AI", "Human vs Human"]

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        w, h = screen.get_size()

        largeSpace = 0.03 * h
        smallSpace = 0.015 * h
        mx, my = pygame.mouse.get_pos()
        y = 70

        # ── Title ──────────────────────────────────────────────
        title = font_title.render("Hnefatafl", True, ACCENT)
        screen.blit(title, (w // 2 - title.get_width() // 2, y))
        sub = font_hint.render("Viking Chess  ·  AI", True, DIM_COLOR)
        screen.blit(sub, (w // 2 - sub.get_width() // 2, y + title.get_height() + 4))

        y += h // 4 - y

        # ── Game Mode section ──────────────────────────────────
        head = font_head.render("Game Mode", True, TEXT_COLOR)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        mode_rects = {}
        btn_w, btn_h, gap = 160, 38, 12
        total = len(modes) * btn_w + (len(modes) - 1) * gap
        bx = w // 2 - total // 2

        for mode in modes:
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            mode_rects[mode] = rect
            is_sel   = mode == selected_mode
            is_hover = rect.collidepoint(mx, my)
            bg     = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
            border = ACCENT if is_sel else (80, 68, 44)

            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)

            label = font_btn.render(mode, True, ACCENT if is_sel else TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap

        y += btn_h + largeSpace
        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += smallSpace

        # ── Role section (always active) ───────────────────────
        # role_active: always True — user always picks a side
        role_active = True

        head = font_head.render("Choose Your Side", True, TEXT_COLOR)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        role_rects = {}
        btn_w = 140
        total = len(ROLES) * btn_w + (len(ROLES) - 1) * gap
        bx = w // 2 - total // 2

        for role in ROLES.keys():
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            role_rects[role] = rect
            is_sel   = role == selected_role
            is_hover = rect.collidepoint(mx, my)
            bg     = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
            border = ACCENT if is_sel else (80, 68, 44)
            label  = font_btn.render(role, True, ACCENT if is_sel else TEXT_COLOR)

            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap

        y += btn_h + largeSpace
        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += smallSpace

        # ── Difficulty section (only active in Human vs AI) ────
        # diff_active: only relevant when playing against AI
        diff_active = selected_mode == "Human vs AI"

        head_color = TEXT_COLOR if diff_active else DIM_COLOR
        head = font_head.render("Difficulty", True, head_color)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        diff_rects = {}
        total = len(DIFFICULTIES) * btn_w + (len(DIFFICULTIES) - 1) * gap
        bx = w // 2 - total // 2

        for diff in DIFFICULTIES.keys():
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            diff_rects[diff] = rect

            if not diff_active:
                # Greyed out — no AI to set difficulty for
                bg     = (35, 30, 24)
                border = (55, 48, 36)
                label  = font_btn.render(diff, True, DIM_COLOR)
            else:
                is_sel   = diff == selected_difficulty
                is_hover = rect.collidepoint(mx, my)
                bg     = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
                border = ACCENT if is_sel else (80, 68, 44)
                label  = font_btn.render(diff, True, ACCENT if is_sel else TEXT_COLOR)

            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap

        y += btn_h + largeSpace
        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += smallSpace

        # ── Board Size section ─────────────────────────────────
        head = font_head.render("Board Size", True, TEXT_COLOR)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        board_sizes = [9, 11]
        board_rects = {}

        total = len(board_sizes) * btn_w + (len(board_sizes) - 1) * gap
        bx = w // 2 - total // 2

        for size in board_sizes:
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            board_rects[size] = rect
            is_sel   = size == selected_board_size
            is_hover = rect.collidepoint(mx, my)

            bg     = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
            border = ACCENT if is_sel else (80, 68, 44)

            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)

            label = font_btn.render(f"{size} x {size}", True,
                                    ACCENT if is_sel else TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap

        y += btn_h + largeSpace
        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += largeSpace

        # ── Start button ───────────────────────────────────────
        start_rect = pygame.Rect(w // 2 - 90, y, 200, 44)
        is_hover = start_rect.collidepoint(mx, my)

        pygame.draw.rect(screen, (HOVER_COLOR if is_hover else (40, 34, 26)),
                         start_rect, border_radius=8)
        pygame.draw.rect(screen, ACCENT, start_rect, 2, border_radius=8)

        sl = font_head.render("Start Game", True, ACCENT)
        screen.blit(sl, (start_rect.centerx - sl.get_width() // 2,
                         start_rect.centery - sl.get_height() // 2))

        # ── Events ─────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return selected_mode, selected_role, selected_difficulty, selected_board_size

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Mode selection
                for mode, rect in mode_rects.items():
                    if rect.collidepoint(mx, my):
                        selected_mode = mode

                # Role selection (always active)
                for role, rect in role_rects.items():
                    if rect.collidepoint(mx, my):
                        selected_role = role

                # Difficulty selection (only active in Human vs AI)
                if diff_active:
                    for diff, rect in diff_rects.items():
                        if rect.collidepoint(mx, my):
                            selected_difficulty = diff

                # Board size selection
                for size, rect in board_rects.items():
                    if rect.collidepoint(mx, my):
                        selected_board_size = size

                if start_rect.collidepoint(mx, my):
                    return selected_mode, ROLES[selected_role], selected_difficulty, selected_board_size

        pygame.display.flip()
        clock.tick(60)