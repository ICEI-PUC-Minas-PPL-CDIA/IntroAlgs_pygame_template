import math
import pygame
import settings as S


class Snake:
    def __init__(self, pos, sounds, particles):
        self.sounds = sounds
        self.particles = particles

        self.head = pygame.Vector2(pos)
        self.direction = pygame.Vector2(1, 0)
        self.pending_direction = pygame.Vector2(1, 0)

        self.base_speed = S.SNAKE_SPEED_INITIAL
        self.speed = S.SNAKE_SPEED_INITIAL

        self.path = [self.head.copy()]
        self.segment_count = S.START_SEGMENTS
        self.segment_positions = []

        self.score = 0
        self.lives = S.START_LIVES

        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dashing = False

        self.ghost_timer = 0.0
        self.invert_timer = 0.0
        self.pepper_timer = 0.0
        self.ice_timer = 0.0

        self.invulnerable = 0.0

        self._rebuild_segments()

    @property
    def ghost_mode(self):
        return self.ghost_timer > 0

    @property
    def controls_inverted(self):
        return self.invert_timer > 0

    @property
    def speed_boost(self):
        return self.pepper_timer > 0

    @property
    def radius(self):
        return S.HEAD_RADIUS

    def set_input_direction(self, vec):
        if vec.length_squared() == 0:
            return
        v = vec.normalize()
        if self.controls_inverted:
            v = -v
        if v.dot(self.direction) < -0.9 and self.segment_count > 1 and not self.ghost_mode:
            return
        self.pending_direction = v

    def try_dash(self):
        if self.dash_cooldown > 0 or self.dashing:
            return
        if self.segment_count > 1:
            self.segment_count -= S.DASH_COST_SEGMENTS
        elif self.score >= S.DASH_COST_POINTS:
            self.score -= S.DASH_COST_POINTS
        else:
            return
        self.dashing = True
        self.dash_timer = S.DASH_DURATION
        self.dash_cooldown = S.DASH_COOLDOWN
        self.sounds["dash"].play()

    def grow(self, amount=1):
        self.segment_count += amount

    def cut_tail(self, amount):
        self.segment_count = max(1, self.segment_count - amount)

    def apply_effect(self, kind):
        if kind == "pepper":
            self.pepper_timer = S.PEPPER_DURATION
            self.ice_timer = 0.0
            self.sounds["powerup"].play()
        elif kind == "ice":
            self.ice_timer = S.ICE_DURATION
            self.pepper_timer = 0.0
            self.sounds["powerdown"].play()
        elif kind == "mushroom":
            self.invert_timer = S.MUSHROOM_DURATION
            self.sounds["powerdown"].play()
        elif kind == "scissors":
            self.cut_tail(S.SCISSORS_CUT)
            self.sounds["powerup"].play()
        elif kind == "ghost":
            self.ghost_timer = S.GHOST_DURATION
            self.sounds["powerup"].play()

    def _current_speed(self):
        spd = self.base_speed
        if self.pepper_timer > 0:
            spd *= S.PEPPER_MULT
        if self.ice_timer > 0:
            spd *= S.ICE_MULT
        spd = min(spd, S.SNAKE_SPEED_MAX)
        if self.dashing:
            spd = S.DASH_SPEED
        return spd

    def update(self, dt):
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        self.ghost_timer = max(0.0, self.ghost_timer - dt)
        self.invert_timer = max(0.0, self.invert_timer - dt)
        self.pepper_timer = max(0.0, self.pepper_timer - dt)
        self.ice_timer = max(0.0, self.ice_timer - dt)
        self.invulnerable = max(0.0, self.invulnerable - dt)

        if self.dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.dashing = False

        angle = self.direction.angle_to(self.pending_direction)
        turn_rate = 540.0 * dt
        if abs(angle) <= turn_rate:
            self.direction = self.pending_direction.copy()
        else:
            self.direction = self.direction.rotate(turn_rate if angle > 0 else -turn_rate)
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.speed = self._current_speed()
        self.head += self.direction * self.speed * dt

        self._clamp_to_arena()
        self._record_path()
        self._rebuild_segments()

        if self.dashing:
            self.particles.trail(self.head, S.C_DASH_READY, count=3, life=0.35, radius=8)
        if self.ghost_mode:
            self.particles.trail(self.head, S.C_GHOST, count=1, life=0.3, radius=6)

    def _clamp_to_arena(self):
        x, y, w, h = S.ARENA_RECT
        r = S.HEAD_RADIUS
        if not self.ghost_mode:
            return
        if self.head.x < x + r:
            self.head.x = x + r
        if self.head.x > x + w - r:
            self.head.x = x + w - r
        if self.head.y < y + r:
            self.head.y = y + r
        if self.head.y > y + h - r:
            self.head.y = y + h - r

    def hits_arena_bounds(self):
        x, y, w, h = S.ARENA_RECT
        r = S.HEAD_RADIUS
        return (self.head.x < x + r or self.head.x > x + w - r or
                self.head.y < y + r or self.head.y > y + h - r)

    def _record_path(self):
        if (self.head - self.path[0]).length() >= 2:
            self.path.insert(0, self.head.copy())
        max_points = int((self.segment_count + 2) * S.SEGMENT_SPACING / 2) + 60
        if len(self.path) > max_points:
            self.path = self.path[:max_points]

    def _rebuild_segments(self):
        self.segment_positions = []
        if len(self.path) < 2:
            for _ in range(self.segment_count):
                self.segment_positions.append(self.head.copy())
            return
        target = S.SEGMENT_SPACING
        seg_index = 0
        accumulated = 0.0
        i = 0
        while seg_index < self.segment_count and i < len(self.path) - 1:
            a = self.path[i]
            b = self.path[i + 1]
            d = (b - a).length()
            if d == 0:
                i += 1
                continue
            while accumulated + d >= target and seg_index < self.segment_count:
                remain = target - accumulated
                frac = remain / d
                point = a + (b - a) * frac
                self.segment_positions.append(point)
                seg_index += 1
                target += S.SEGMENT_SPACING
            accumulated += d
            i += 1
        while seg_index < self.segment_count:
            self.segment_positions.append(self.path[-1].copy())
            seg_index += 1

    def self_collision(self):
        if self.ghost_mode or self.segment_count < 8:
            return False
        skip = 5
        for seg in self.segment_positions[skip:]:
            if (self.head - seg).length() < S.SEGMENT_RADIUS:
                return True
        return False

    def lose_life(self):
        self.lives -= 1
        self.invulnerable = 1.5
        self.sounds["hurt"].play()

    def respawn(self, pos):
        self.head = pygame.Vector2(pos)
        self.direction = pygame.Vector2(1, 0)
        self.pending_direction = pygame.Vector2(1, 0)
        self.path = [self.head.copy()]
        self.segment_count = max(S.START_SEGMENTS, self.segment_count - 3)
        self.dashing = False
        self.dash_timer = 0.0
        self.ghost_timer = 0.0
        self.invert_timer = 0.0
        self._rebuild_segments()

    def draw(self, surface):
        blink = self.invulnerable > 0 and int(self.invulnerable * 12) % 2 == 0
        if blink:
            return

        for i in range(len(self.segment_positions) - 1, -1, -1):
            seg = self.segment_positions[i]
            t = i / max(1, len(self.segment_positions))
            if self.ghost_mode:
                base = S.C_GHOST
                col = (int(base[0] * (1 - t * 0.4)),
                       int(base[1] * (1 - t * 0.4)),
                       int(base[2]))
            else:
                col = (int(S.C_SNAKE[0] * (1 - t * 0.4) + S.C_SNAKE_DARK[0] * t * 0.4),
                       int(S.C_SNAKE[1] * (1 - t * 0.4) + S.C_SNAKE_DARK[1] * t * 0.4),
                       int(S.C_SNAKE[2] * (1 - t * 0.4) + S.C_SNAKE_DARK[2] * t * 0.4))
            pygame.draw.circle(surface, col, (int(seg.x), int(seg.y)), S.SEGMENT_RADIUS)

        head_col = S.C_GHOST if self.ghost_mode else S.C_SNAKE_HEAD
        if self.ghost_mode:
            glow = pygame.Surface((S.HEAD_RADIUS * 4, S.HEAD_RADIUS * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (140, 200, 255, 80), (S.HEAD_RADIUS * 2, S.HEAD_RADIUS * 2), S.HEAD_RADIUS * 2)
            surface.blit(glow, (self.head.x - S.HEAD_RADIUS * 2, self.head.y - S.HEAD_RADIUS * 2))
        pygame.draw.circle(surface, head_col, (int(self.head.x), int(self.head.y)), S.HEAD_RADIUS)

        eye_offset = self.direction.rotate(90) * 5
        forward = self.direction * 5
        e1 = self.head + forward + eye_offset
        e2 = self.head + forward - eye_offset
        pygame.draw.circle(surface, (20, 20, 30), (int(e1.x), int(e1.y)), 3)
        pygame.draw.circle(surface, (20, 20, 30), (int(e2.x), int(e2.y)), 3)
