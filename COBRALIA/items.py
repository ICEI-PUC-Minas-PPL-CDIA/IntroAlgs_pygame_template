import math
import random
import pygame
import settings as S


class Item:
    RADIUS = 13

    def __init__(self, kind, pos):
        self.kind = kind
        self.pos = pygame.Vector2(pos)
        self.time = 0.0
        self.collected = False

    @property
    def color(self):
        return {
            "apple": S.C_APPLE,
            "pepper": S.C_PEPPER,
            "ice": S.C_ICE,
            "mushroom": S.C_MUSHROOM,
            "scissors": S.C_SCISSORS,
            "ghost": S.C_GHOST_ITEM,
        }[self.kind]

    def update(self, dt):
        self.time += dt

    def collides_with(self, point, point_radius):
        return (self.pos - point).length() < self.RADIUS + point_radius

    def draw(self, surface):
        bob = math.sin(self.time * 3) * 3
        cx, cy = int(self.pos.x), int(self.pos.y + bob)
        col = self.color

        if self.kind == "apple":
            pygame.draw.circle(surface, col, (cx, cy), self.RADIUS)
            pygame.draw.circle(surface, (255, 160, 160), (cx - 4, cy - 4), 3)
            pygame.draw.line(surface, (90, 200, 90), (cx, cy - self.RADIUS),
                             (cx + 5, cy - self.RADIUS - 6), 3)
        elif self.kind == "pepper":
            pygame.draw.polygon(surface, col, [(cx - 8, cy - 8), (cx + 8, cy - 4),
                                               (cx + 4, cy + 10), (cx - 6, cy + 6)])
            pygame.draw.line(surface, (90, 200, 90), (cx - 8, cy - 8), (cx - 12, cy - 14), 3)
        elif self.kind == "ice":
            pts = []
            for i in range(6):
                a = math.radians(i * 60)
                pts.append((cx + math.cos(a) * self.RADIUS, cy + math.sin(a) * self.RADIUS))
            pygame.draw.polygon(surface, col, pts)
            pygame.draw.polygon(surface, (255, 255, 255), pts, 2)
        elif self.kind == "mushroom":
            pygame.draw.circle(surface, col, (cx, cy - 2), self.RADIUS)
            pygame.draw.rect(surface, (240, 230, 210), (cx - 5, cy, 10, 10), border_radius=3)
            pygame.draw.circle(surface, (255, 255, 255), (cx - 4, cy - 4), 2)
            pygame.draw.circle(surface, (255, 255, 255), (cx + 4, cy - 2), 2)
        elif self.kind == "scissors":
            pygame.draw.line(surface, col, (cx - 8, cy - 8), (cx + 8, cy + 8), 3)
            pygame.draw.line(surface, col, (cx + 8, cy - 8), (cx - 8, cy + 8), 3)
            pygame.draw.circle(surface, col, (cx - 8, cy + 8), 4, 2)
            pygame.draw.circle(surface, col, (cx + 8, cy + 8), 4, 2)
        elif self.kind == "ghost":
            pygame.draw.circle(surface, col, (cx, cy - 2), self.RADIUS)
            pygame.draw.rect(surface, col, (cx - self.RADIUS, cy - 2, self.RADIUS * 2, self.RADIUS))
            pygame.draw.circle(surface, (40, 40, 60), (cx - 4, cy - 4), 3)
            pygame.draw.circle(surface, (40, 40, 60), (cx + 4, cy - 4), 3)

        glow = pygame.Surface((self.RADIUS * 4, self.RADIUS * 4), pygame.SRCALPHA)
        a = int(50 + 30 * math.sin(self.time * 4))
        pygame.draw.circle(glow, (col[0], col[1], col[2], a),
                           (self.RADIUS * 2, self.RADIUS * 2), self.RADIUS * 2)
        surface.blit(glow, (cx - self.RADIUS * 2, cy - self.RADIUS * 2),
                     special_flags=pygame.BLEND_RGBA_ADD)


def random_arena_point(margin=40):
    x, y, w, h = S.ARENA_RECT
    return pygame.Vector2(random.uniform(x + margin, x + w - margin),
                          random.uniform(y + margin, y + h - margin))


def pick_special_kind():
    roll = random.random()
    cumulative = 0.0
    for kind, chance in S.SPECIAL_ITEM_CHANCE.items():
        cumulative += chance
        if roll < cumulative:
            return kind
    return None
