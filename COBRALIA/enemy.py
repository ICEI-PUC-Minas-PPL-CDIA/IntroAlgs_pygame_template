import math
import pygame
import settings as S


class Predator:
    RADIUS = 16

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2()
        self.speed = S.PREDATOR_SPEED
        self.time = 0.0
        self.chasing = False

    def _avoid_walls(self, desired, walls):
        candidate = self.pos + desired * 4
        for w in walls:
            if w.collides_circle(candidate, self.RADIUS):
                for angle in (35, -35, 70, -70, 110, -110, 150, -150):
                    alt = desired.rotate(angle)
                    if not w.collides_circle(self.pos + alt * 4, self.RADIUS):
                        return alt
        return desired

    def update(self, dt, target, walls):
        self.time += dt
        to_target = target - self.pos
        dist = to_target.length()
        self.chasing = dist <= S.PREDATOR_DETECT_RADIUS

        if self.chasing and dist > 0:
            desired = to_target.normalize()
            desired = self._avoid_walls(desired, walls)
            self.vel = desired * self.speed
        else:
            self.vel *= 0.9

        nxt = self.pos + self.vel * dt
        blocked = any(w.collides_circle(nxt, self.RADIUS) for w in walls)
        if not blocked:
            self.pos = nxt

        x, y, w, h = S.ARENA_RECT
        self.pos.x = max(x + self.RADIUS, min(self.pos.x, x + w - self.RADIUS))
        self.pos.y = max(y + self.RADIUS, min(self.pos.y, y + h - self.RADIUS))

    def caught(self, point, radius):
        return (self.pos - point).length() < self.RADIUS + radius

    def draw(self, surface):
        cx, cy = int(self.pos.x), int(self.pos.y)
        if self.chasing:
            glow = pygame.Surface((self.RADIUS * 4, self.RADIUS * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (230, 60, 90, 70),
                               (self.RADIUS * 2, self.RADIUS * 2), self.RADIUS * 2)
            surface.blit(glow, (cx - self.RADIUS * 2, cy - self.RADIUS * 2))
        pygame.draw.circle(surface, S.C_PREDATOR, (cx, cy), self.RADIUS)
        pygame.draw.circle(surface, (120, 20, 40), (cx, cy), self.RADIUS, 2)

        if self.vel.length_squared() > 0:
            d = self.vel.normalize()
        else:
            d = pygame.Vector2(1, 0)
        for s in (1, -1):
            base = self.pos + d.rotate(90 * s) * 6 - d * 4
            tip = base - d * 10 + d.rotate(90 * s) * 4
            pygame.draw.polygon(surface, (160, 30, 50),
                                [(base.x, base.y), (tip.x, tip.y),
                                 (base.x - d.x * 2, base.y - d.y * 2)])
        eye = self.pos + d * 6
        pygame.draw.circle(surface, (255, 230, 100), (int(eye.x), int(eye.y)), 4)
        pygame.draw.circle(surface, (20, 0, 0), (int(eye.x), int(eye.y)), 2)
