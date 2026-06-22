import math
import random
import pygame
import settings as S
from walls import Wall


class Projectile:
    RADIUS = 9

    def __init__(self, pos, vel):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.alive = True

    def update(self, dt):
        self.pos += self.vel * dt
        x, y, w, h = S.ARENA_RECT
        if not (x < self.pos.x < x + w and y < self.pos.y < y + h):
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 120, 60),
                           (int(self.pos.x), int(self.pos.y)), self.RADIUS)
        pygame.draw.circle(surface, (255, 220, 160),
                           (int(self.pos.x), int(self.pos.y)), self.RADIUS - 4)


class Boss:
    HEAD_RADIUS = 38
    BODY_SEGMENTS = 8
    WEAK_RADIUS = 18

    def __init__(self):
        x, y, w, h = S.ARENA_RECT
        self.center = pygame.Vector2(x + w / 2, y + 120)
        self.head = self.center.copy()
        self.time = 0.0
        self.hp = S.BOSS_MAX_HP
        self.max_hp = S.BOSS_MAX_HP

        self.body = [self.head.copy() for _ in range(self.BODY_SEGMENTS)]

        self.weak_open = False
        self.weak_timer = S.BOSS_WEAK_CLOSED_TIME
        self.hit_cooldown = 0.0

        self.attack_index = 0
        self.attack_timer = 2.0
        self.state = "patrol"
        self.charge_target = None
        self.charge_speed = 0.0

        self.projectiles = []
        self.spawned_walls = []
        self.temp_walls = []

        self.dead = False
        self.death_timer = 0.0
        self.exploded = False

        self.sound_request = None

    @property
    def weak_pos(self):
        return self.head + pygame.Vector2(0, self.HEAD_RADIUS + 6)

    def _patrol_target(self):
        x, y, w, h = S.ARENA_RECT
        px = x + w / 2 + math.sin(self.time * 0.8) * (w / 2 - 120)
        py = y + 120 + math.sin(self.time * 1.4) * 50
        return pygame.Vector2(px, py)

    def take_damage(self, particles):
        if self.hit_cooldown > 0 or self.dead:
            return False
        self.hp -= 1
        self.hit_cooldown = 1.2
        self.weak_open = False
        self.weak_timer = S.BOSS_WEAK_CLOSED_TIME
        self.sound_request = "hit"
        particles.burst(self.weak_pos, S.C_BOSS_WEAK_OPEN, count=24, speed=240)
        if self.hp <= 0:
            self.dead = True
            self.death_timer = 2.2
            particles.explosion(self.head, count=120)
            self.sound_request = "boss_dead"
        return True

    def _update_weak(self, dt):
        self.weak_timer -= dt
        if self.weak_timer <= 0:
            self.weak_open = not self.weak_open
            self.weak_timer = S.BOSS_WEAK_OPEN_TIME if self.weak_open else S.BOSS_WEAK_CLOSED_TIME

    def _start_next_attack(self, player):
        self.attack_index = (self.attack_index + 1) % 3
        if self.attack_index == 0:
            self._attack_projectiles(player)
            self.attack_timer = 2.4
        elif self.attack_index == 1:
            self.state = "charge"
            self.charge_target = player.head.copy()
            self.charge_speed = 0.0
            self.attack_timer = 2.0
        else:
            self._attack_walls()
            self.attack_timer = 3.0

    def _attack_projectiles(self, player):
        self.sound_request = "boss_attack"
        base = (player.head - self.head)
        if base.length_squared() == 0:
            base = pygame.Vector2(0, 1)
        base = base.normalize()
        for ang in (-25, -12, 0, 12, 25):
            v = base.rotate(ang) * 280
            self.projectiles.append(Projectile(self.weak_pos, v))

    def _attack_walls(self):
        self.sound_request = "boss_attack"
        x, y, w, h = S.ARENA_RECT
        self.temp_walls = []
        for _ in range(3):
            ww = random.randint(120, 200)
            wx = random.randint(x + 40, x + w - ww - 40)
            wy = random.randint(y + 220, y + h - 80)
            wall = Wall((wx, wy, ww, 24))
            wall.life = 5.0
            self.temp_walls.append(wall)

    def update(self, dt, player, particles):
        self.time += dt
        self.hit_cooldown = max(0.0, self.hit_cooldown - dt)

        if self.dead:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.exploded = True
            if random.random() < 0.4:
                off = pygame.Vector2(random.uniform(-40, 40), random.uniform(-40, 40))
                particles.burst(self.head + off, (255, 160, 60), count=10, speed=160)
            return

        self._update_weak(dt)

        if self.state == "patrol":
            target = self._patrol_target()
            self.head += (target - self.head) * min(1.0, 2.5 * dt)
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self._start_next_attack(player)
        elif self.state == "charge":
            self.charge_speed = min(620.0, self.charge_speed + 900 * dt)
            to_target = self.charge_target - self.head
            if to_target.length() < 20 or self.attack_timer <= 0:
                self.state = "patrol"
                self.attack_timer = 1.5
            else:
                self.head += to_target.normalize() * self.charge_speed * dt
            self.attack_timer -= dt

        self._update_body()

        for p in self.projectiles:
            p.update(dt)
        self.projectiles = [p for p in self.projectiles if p.alive]

        for w in self.temp_walls:
            w.life -= dt
        self.temp_walls = [w for w in self.temp_walls if w.life > 0]

    def _update_body(self):
        prev = self.head
        spacing = 26
        for i, seg in enumerate(self.body):
            to_prev = prev - seg
            d = to_prev.length()
            if d > spacing:
                seg += to_prev.normalize() * (d - spacing)
            prev = seg

    def check_projectile_hits(self, player):
        for p in self.projectiles:
            if (p.pos - player.head).length() < Projectile.RADIUS + player.radius:
                p.alive = False
                return True
        return False

    def check_charge_hit(self, player):
        if self.state == "charge":
            if (self.head - player.head).length() < self.HEAD_RADIUS + player.radius:
                return True
        return False

    def check_weak_hit(self, player, particles):
        if self.weak_open and self.hit_cooldown <= 0:
            if (self.weak_pos - player.head).length() < self.WEAK_RADIUS + player.radius:
                return self.take_damage(particles)
        return False

    def all_collision_walls(self):
        return self.temp_walls

    def draw(self, surface):
        if self.exploded:
            return

        for i in range(len(self.body) - 1, -1, -1):
            seg = self.body[i]
            t = i / len(self.body)
            r = int(28 * (1 - t * 0.5))
            col = (int(S.C_BOSS[0] * (1 - t * 0.3)),
                   int(S.C_BOSS[1] * (1 - t * 0.3)),
                   int(S.C_BOSS[2] * (1 - t * 0.3)))
            pygame.draw.circle(surface, col, (int(seg.x), int(seg.y)), r)
            pygame.draw.circle(surface, (200, 210, 240), (int(seg.x), int(seg.y)), r, 2)

        for w in self.temp_walls:
            w.draw(surface)

        cx, cy = int(self.head.x), int(self.head.y)
        flash = self.hit_cooldown > 0 and int(self.hit_cooldown * 12) % 2 == 0
        head_col = (255, 255, 255) if flash else S.C_BOSS
        pygame.draw.circle(surface, head_col, (cx, cy), self.HEAD_RADIUS)
        pygame.draw.circle(surface, (90, 100, 140), (cx, cy), self.HEAD_RADIUS, 3)

        for s in (-1, 1):
            ex = cx + s * 14
            ey = cy - 8
            pygame.draw.circle(surface, (255, 80, 60), (ex, ey), 6)
            pygame.draw.circle(surface, (255, 200, 120), (ex, ey), 2)

        wp = self.weak_pos
        if self.weak_open:
            pulse = int(6 * math.sin(self.time * 12))
            glow = pygame.Surface((self.WEAK_RADIUS * 4, self.WEAK_RADIUS * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 200, 60, 120),
                               (self.WEAK_RADIUS * 2, self.WEAK_RADIUS * 2), self.WEAK_RADIUS * 2)
            surface.blit(glow, (wp.x - self.WEAK_RADIUS * 2, wp.y - self.WEAK_RADIUS * 2),
                         special_flags=pygame.BLEND_RGBA_ADD)
            pygame.draw.circle(surface, S.C_BOSS_WEAK_OPEN,
                               (int(wp.x), int(wp.y)), self.WEAK_RADIUS + pulse)
            pygame.draw.circle(surface, (255, 255, 200),
                               (int(wp.x), int(wp.y)), self.WEAK_RADIUS // 2)
        else:
            pygame.draw.circle(surface, S.C_BOSS_WEAK, (int(wp.x), int(wp.y)), self.WEAK_RADIUS)
            pygame.draw.circle(surface, (120, 30, 30), (int(wp.x), int(wp.y)), self.WEAK_RADIUS, 3)

        for p in self.projectiles:
            p.draw(surface)
