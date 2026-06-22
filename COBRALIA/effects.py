import random
import pygame


class Particle:
    def __init__(self, pos, vel, color, life, radius):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.color = color
        self.life = life
        self.max_life = life
        self.radius = radius

    def update(self, dt):
        self.pos += self.vel * dt
        self.vel *= 0.92
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        if self.life <= 0:
            return
        frac = max(0.0, self.life / self.max_life)
        r = max(1, int(self.radius * frac))
        c = (int(self.color[0]), int(self.color[1]), int(self.color[2]))
        pygame.draw.circle(surface, c, (int(self.pos.x), int(self.pos.y)), r)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, pos, color, count=14, speed=180, life=0.6, radius=5):
        for _ in range(count):
            ang = random.uniform(0, 6.283)
            spd = random.uniform(speed * 0.3, speed)
            vel = (pygame.math.Vector2(1, 0)).rotate_rad(ang) * spd
            self.particles.append(Particle(pos, vel, color, random.uniform(life * 0.5, life), radius))

    def trail(self, pos, color, count=2, life=0.4, radius=6):
        for _ in range(count):
            vel = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
            self.particles.append(Particle(pos, vel, color, life, radius))

    def explosion(self, pos, count=80):
        colors = [(255, 200, 60), (255, 120, 40), (230, 60, 60), (255, 255, 200)]
        for _ in range(count):
            ang = random.uniform(0, 6.283)
            spd = random.uniform(60, 360)
            vel = pygame.Vector2(1, 0).rotate_rad(ang) * spd
            col = random.choice(colors)
            self.particles.append(Particle(pos, vel, col, random.uniform(0.5, 1.4), random.uniform(4, 10)))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class ScreenFlash:
    def __init__(self):
        self.timer = 0.0
        self.duration = 0.0
        self.color = (255, 255, 255)

    def trigger(self, color=(255, 60, 60), duration=0.3):
        self.color = color
        self.duration = duration
        self.timer = duration

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def draw(self, surface):
        if self.timer <= 0:
            return
        alpha = int(140 * (self.timer / self.duration))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((self.color[0], self.color[1], self.color[2], alpha))
        surface.blit(overlay, (0, 0))
