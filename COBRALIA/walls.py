import pygame
import settings as S


class Wall:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.lethal_moving = False

    def update(self, dt):
        pass

    def collides_circle(self, center, radius):
        cx = max(self.rect.left, min(center.x, self.rect.right))
        cy = max(self.rect.top, min(center.y, self.rect.bottom))
        return (center.x - cx) ** 2 + (center.y - cy) ** 2 < radius ** 2

    def draw(self, surface):
        pygame.draw.rect(surface, S.C_WALL, self.rect, border_radius=4)
        pygame.draw.rect(surface, (130, 140, 180), self.rect, 2, border_radius=4)


class MovingWall(Wall):
    def __init__(self, rect, axis, speed, travel):
        super().__init__(rect)
        self.lethal_moving = True
        self.axis = axis
        self.speed = speed
        self.travel = travel
        self.origin = pygame.Vector2(self.rect.topleft)
        self.offset = 0.0
        self.dirsign = 1

    def update(self, dt):
        self.offset += self.speed * self.dirsign * dt
        if self.offset > self.travel:
            self.offset = self.travel
            self.dirsign = -1
        elif self.offset < 0:
            self.offset = 0
            self.dirsign = 1
        if self.axis == "h":
            self.rect.x = int(self.origin.x + self.offset)
        else:
            self.rect.y = int(self.origin.y + self.offset)

    def draw(self, surface):
        pygame.draw.rect(surface, S.C_WALL_MOVING, self.rect, border_radius=4)
        pygame.draw.rect(surface, (255, 180, 110), self.rect, 2, border_radius=4)
        for i in range(3):
            x = self.rect.x + 8 + i * (self.rect.width // 3)
            pygame.draw.line(surface, (255, 200, 140),
                             (x, self.rect.y + 4), (x, self.rect.bottom - 4), 2)
