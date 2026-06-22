import random
import pygame
import settings as S
from walls import Wall, MovingWall


def _arena():
    return S.ARENA_RECT


def build_level(level_cfg):
    walls = []
    x, y, w, h = _arena()
    level_id = level_cfg["id"]

    if level_cfg.get("boss"):
        walls.append(Wall((x + 60, y + h - 60, 200, 24)))
        walls.append(Wall((x + w - 260, y + h - 60, 200, 24)))
        return walls

    random.seed(level_id * 1337)

    if level_id >= 2:
        walls.append(Wall((x + w // 2 - 100, y + h // 2 - 14, 200, 28)))
    if level_id >= 3:
        walls.append(Wall((x + 120, y + 120, 28, 160)))
        walls.append(Wall((x + w - 148, y + h - 280, 28, 160)))
    if level_id >= 4:
        walls.append(Wall((x + w // 2 - 14, y + 80, 28, 140)))
        walls.append(Wall((x + w // 2 - 14, y + h - 220, 28, 140)))

    moving_count = level_cfg.get("moving_walls", 0)
    for i in range(moving_count):
        if i % 2 == 0:
            rx = x + 100 + (i * 90) % (w - 300)
            wall = MovingWall((rx, y + 90, 90, 26), "v",
                              speed=80 + i * 15, travel=h - 220)
        else:
            ry = y + 120 + (i * 110) % (h - 300)
            wall = MovingWall((x + 90, ry, 26, 90), "h",
                              speed=90 + i * 15, travel=w - 220)
        walls.append(wall)

    random.seed()
    return walls


def safe_spawn(walls, attempts=200):
    x, y, w, h = _arena()
    center = pygame.Vector2(x + 120, y + h // 2)
    for _ in range(attempts):
        ok = True
        for wall in walls:
            if wall.collides_circle(center, 60):
                ok = False
                break
        if ok:
            return center
        center = pygame.Vector2(random.uniform(x + 80, x + w - 80),
                                random.uniform(y + 80, y + h - 80))
    return pygame.Vector2(x + 120, y + h // 2)
