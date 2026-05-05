import pygame
import sys
from constants import DIFFICULTIES, ROLES

BG_COLOR     = (30, 25, 20)
TEXT_COLOR   = (220, 210, 190)
DIM_COLOR    = (120, 110, 90)
ACCENT       = (210, 165, 40)
HOVER_COLOR  = (60, 50, 35)
SELECT_COLOR = (80, 65, 30)



def run_menu(screen) -> tuple[str, str]:
    """Blocks until the user confirms. Returns (role, difficulty)."""
    font_title = pygame.font.SysFont("Segoe UI", 40, bold=True)
    font_head  = pygame.font.SysFont("Segoe UI", 25, bold=True)
    font_btn   = pygame.font.SysFont("Segoe UI", 17)
    font_hint  = pygame.font.SysFont("Segoe UI", 17)

    selected_role       = "Attacker"
    selected_difficulty = "Medium"
    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        w, h = screen.get_size()
        
        largeSpace = 0.05 * h
        smallSpace = 0.025 * h
        mx, my = pygame.mouse.get_pos()
        y = 70

        # ── Title ──────────────────────────────────────────────
        title = font_title.render("Hnefatafl", True, ACCENT)
        screen.blit(title, (w // 2 - title.get_width() // 2, y))
        sub = font_hint.render("Viking Chess  ·  AI", True, DIM_COLOR)
        screen.blit(sub, (w // 2 - sub.get_width() // 2, y + title.get_height() + 4))

        y += h // 4 - y
        # pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        # y += 18

        # ── Role section ───────────────────────────────────────
        head = font_head.render("Choose Your Side", True, TEXT_COLOR)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        role_rects = {}
        btn_w, btn_h, gap = 140, 38, 12
        total = len(ROLES) * btn_w + (len(ROLES) - 1) * gap
        bx = w // 2 - total // 2
        for role in ROLES.keys():
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            role_rects[role] = rect
            is_sel   = role == selected_role
            is_hover = rect.collidepoint(mx, my)
            bg = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
            border = ACCENT if is_sel else (80, 68, 44)
            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)
            label = font_btn.render(role, True, ACCENT if is_sel else TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap
        y += btn_h + largeSpace

        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += smallSpace

        # ── Difficulty section ─────────────────────────────────
        head = font_head.render("Difficulty", True, TEXT_COLOR)
        screen.blit(head, (w // 2 - head.get_width() // 2, y))
        y += head.get_height() + smallSpace

        diff_rects = {}
        total = len(DIFFICULTIES) * btn_w + (len(DIFFICULTIES) - 1) * gap
        bx = w // 2 - total // 2
        for diff in DIFFICULTIES.keys():
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            diff_rects[diff] = rect
            is_sel   = diff == selected_difficulty
            is_hover = rect.collidepoint(mx, my)
            bg = SELECT_COLOR if is_sel else (HOVER_COLOR if is_hover else (40, 34, 26))
            border = ACCENT if is_sel else (80, 68, 44)
            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, border, rect, 1, border_radius=6)
            label = font_btn.render(diff, True, ACCENT if is_sel else TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2,
                                rect.centery - label.get_height() // 2))
            bx += btn_w + gap
        y += btn_h + largeSpace

        pygame.draw.line(screen, (60, 50, 35), (40, y), (w - 40, y), 1)
        y += largeSpace

        # ── Start button ───────────────────────────────────────
        start_rect = pygame.Rect(w // 2 - 90, y, 200, 44)
        is_hover   = start_rect.collidepoint(mx, my)
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
                return selected_role, selected_difficulty
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for role, rect in role_rects.items():
                    if rect.collidepoint(mx, my):
                        selected_role = role
                for diff, rect in diff_rects.items():
                    if rect.collidepoint(mx, my):
                        selected_difficulty = diff
                if start_rect.collidepoint(mx, my):
                    return selected_role, selected_difficulty

        pygame.display.flip()
        clock.tick(60)