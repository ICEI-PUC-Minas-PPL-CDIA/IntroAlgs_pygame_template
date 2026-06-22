import pygame
import settings as S


class Button:
    def __init__(self, text, center, size=(300, 60), font=None):
        self.text = text
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center
        self.font = font
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        bg = (50, 60, 95) if self.hovered else S.C_HUD
        border = S.C_HUD_ACCENT if self.hovered else S.C_DARKGREY
        pygame.draw.rect(surface, bg, self.rect, border_radius=10)
        pygame.draw.rect(surface, border, self.rect, 3, border_radius=10)
        label = self.font.render(self.text, True, S.C_WHITE)
        surface.blit(label, label.get_rect(center=self.rect.center))


class Bar:
    def __init__(self):
        self.display = 0.0

    def update(self, target, dt, speed=6.0):
        self.display += (target - self.display) * min(1.0, speed * dt)

    def draw(self, surface, rect, color, bg=S.C_DARKGREY, border=True):
        pygame.draw.rect(surface, bg, rect, border_radius=6)
        inner = pygame.Rect(rect.x + 2, rect.y + 2,
                            int((rect.width - 4) * max(0.0, min(1.0, self.display))),
                            rect.height - 4)
        if inner.width > 0:
            pygame.draw.rect(surface, color, inner, border_radius=6)
        if border:
            pygame.draw.rect(surface, S.C_GREY, rect, 2, border_radius=6)


def draw_text(surface, font, text, pos, color=S.C_WHITE, center=False, shadow=True):
    if shadow:
        sh = font.render(text, True, (10, 12, 20))
        r = sh.get_rect()
        if center:
            r.center = (pos[0] + 2, pos[1] + 2)
        else:
            r.topleft = (pos[0] + 2, pos[1] + 2)
        surface.blit(sh, r)
    label = font.render(text, True, color)
    r = label.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surface.blit(label, r)
    return r


class HUD:
    def __init__(self, fonts):
        self.fonts = fonts
        self.dash_bar = Bar()
        self.boss_bar = Bar()
        self.goal_bar = Bar()
        self.effect_bars = {}

    def update(self, snake, dt, boss=None):
        cd = 1.0 - (snake.dash_cooldown / S.DASH_COOLDOWN) if snake.dash_cooldown > 0 else 1.0
        self.dash_bar.update(cd, dt, 10)
        if boss:
            self.boss_bar.update(boss.hp / boss.max_hp, dt)

    def draw(self, surface, snake, state):
        top = pygame.Rect(0, 0, S.SCREEN_WIDTH, 56)
        pygame.draw.rect(surface, S.C_HUD, top)
        pygame.draw.line(surface, S.C_HUD_ACCENT, (0, 56), (S.SCREEN_WIDTH, 56), 2)

        f = self.fonts["small"]
        draw_text(surface, f, f"FASE {state.level_id}", (20, 16))
        draw_text(surface, f, f"Maças {state.apples}/{state.goal_text}", (150, 16))
        draw_text(surface, f, f"Tamanho {snake.segment_count}", (360, 16))
        draw_text(surface, f, f"Pontos {snake.score}", (540, 16))

        lives_x = 700
        draw_text(surface, f, "Vidas", (lives_x, 16))
        for i in range(snake.lives):
            cx = lives_x + 80 + i * 26
            pygame.draw.circle(surface, S.C_SNAKE, (cx, 28), 9)
            pygame.draw.circle(surface, S.C_SNAKE_HEAD, (cx, 28), 9, 2)

        dash_rect = pygame.Rect(900, 22, 160, 16)
        draw_text(surface, f, "Dash", (900, 2))
        col = S.C_DASH_READY if snake.dash_cooldown <= 0 else S.C_GREY
        self.dash_bar.draw(surface, dash_rect, col)

        self._draw_effects(surface, snake)

        if state.boss:
            self._draw_boss_bar(surface, state.boss)

    def _draw_effects(self, surface, snake):
        f = self.fonts["tiny"]
        x = 1080
        y = 14
        effects = []
        if snake.pepper_timer > 0:
            effects.append(("Pimenta", snake.pepper_timer, S.PEPPER_DURATION, S.C_PEPPER))
        if snake.ice_timer > 0:
            effects.append(("Gelo", snake.ice_timer, S.ICE_DURATION, S.C_ICE))
        if snake.invert_timer > 0:
            effects.append(("Invertido", snake.invert_timer, S.MUSHROOM_DURATION, S.C_MUSHROOM))
        if snake.ghost_timer > 0:
            effects.append(("Fantasma", snake.ghost_timer, S.GHOST_DURATION, S.C_GHOST_ITEM))
        for i, (name, t, total, color) in enumerate(effects):
            ey = y + i * 11
            rect = pygame.Rect(x, ey, 180, 8)
            pygame.draw.rect(surface, S.C_DARKGREY, rect, border_radius=4)
            inner = pygame.Rect(rect.x, rect.y, int(rect.width * (t / total)), rect.height)
            pygame.draw.rect(surface, color, inner, border_radius=4)

    def _draw_boss_bar(self, surface, boss):
        rect = pygame.Rect(S.SCREEN_WIDTH // 2 - 250, 64, 500, 22)
        draw_text(surface, self.fonts["small"], "CHEFÃO",
                  (S.SCREEN_WIDTH // 2, 75), center=True)
        bar_rect = pygame.Rect(S.SCREEN_WIDTH // 2 - 250, 90, 500, 18)
        self.boss_bar.draw(surface, bar_rect, S.C_HP)
