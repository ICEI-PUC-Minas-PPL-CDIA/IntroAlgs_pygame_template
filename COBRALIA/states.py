import math
import random
import pygame
import settings as S
from player import Snake
from items import Item, random_arena_point, pick_special_kind
from walls import Wall, MovingWall
from enemy import Predator
from boss import Boss
from levels import build_level, safe_spawn
from effects import ParticleSystem, ScreenFlash
from ui import Button, HUD, draw_text


class State:
    def __init__(self, game):
        self.game = game

    def on_enter(self, **kwargs):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


def draw_background(surface, t):
    surface.fill(S.C_BG)
    for i in range(0, S.SCREEN_WIDTH, 40):
        shade = 18 + int(6 * math.sin(t * 0.5 + i * 0.05))
        pygame.draw.line(surface, (shade, shade + 4, shade + 14),
                         (i, 0), (i, S.SCREEN_HEIGHT))


class MenuState(State):
    def on_enter(self, **kwargs):
        self.game.play_music("menu")
        cx = S.SCREEN_WIDTH // 2
        f = self.game.fonts["medium"]
        self.buttons = [
            Button("Jogar", (cx, 340), font=f),
            Button("Controles", (cx, 410), font=f),
            Button("Créditos", (cx, 480), font=f),
            Button("Sair", (cx, 550), font=f),
        ]
        self.t = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in self.buttons:
                if b.rect.collidepoint(event.pos):
                    self.game.sounds["select"].play()
                    self._activate(b.text)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.sounds["select"].play()
            self.game.change_state("levelselect")

    def _activate(self, text):
        if text == "Jogar":
            self.game.change_state("levelselect")
        elif text == "Controles":
            self.game.change_state("controls")
        elif text == "Créditos":
            self.game.change_state("credits")
        elif text == "Sair":
            self.game.running = False

    def update(self, dt):
        self.t += dt
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse)

    def draw(self, surface):
        draw_background(surface, self.t)
        cx = S.SCREEN_WIDTH // 2
        bob = math.sin(self.t * 2) * 6
        draw_text(surface, self.game.fonts["title"], "COBRALIA",
                  (cx, 160 + bob), S.C_SNAKE, center=True)
        draw_text(surface, self.game.fonts["medium"], "Snake Ascension",
                  (cx, 230), S.C_GOLD, center=True)
        for b in self.buttons:
            b.draw(surface)
        draw_text(surface, self.game.fonts["tiny"],
                  "Enter para jogar rapido", (cx, 640), S.C_GREY, center=True)


class ControlsState(State):
    def on_enter(self, **kwargs):
        self.t = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN):
            self.game.change_state("menu")

    def update(self, dt):
        self.t += dt

    def draw(self, surface):
        draw_background(surface, self.t)
        cx = S.SCREEN_WIDTH // 2
        draw_text(surface, self.game.fonts["large"], "CONTROLES", (cx, 110), S.C_HUD_ACCENT, center=True)
        lines = [
            "W A S D  -  Mover a cobra",
            "Setas direcionais  -  Mover a cobra",
            "ESPAÇO  -  Dash (impulso rapido)",
            "ESC  -  Pausar / Voltar",
            "",
            "Colete maças para completar cada fase.",
            "Cuidado com paredes, predadores e o chefão.",
        ]
        for i, ln in enumerate(lines):
            draw_text(surface, self.game.fonts["small"], ln, (cx, 220 + i * 50),
                      S.C_WHITE if ln else S.C_GREY, center=True)
        draw_text(surface, self.game.fonts["tiny"], "Pressione qualquer tecla para voltar",
                  (cx, 660), S.C_GREY, center=True)


class CreditsState(State):
    def on_enter(self, **kwargs):
        self.t = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_state("menu")

    def update(self, dt):
        self.t += dt

    def draw(self, surface):
        draw_background(surface, self.t)
        cx = S.SCREEN_WIDTH // 2
        draw_text(surface, self.game.fonts["large"], "CRÉDITOS", (cx, 130), S.C_HUD_ACCENT, center=True)
        lines = [
            "Cobralia: Snake Ascension",
            "",
            "Desenvolvimento  -  Engine Pygame",
            "Programação  -  Python 3.12",
            "Arte  -  Formas geométricas procedurais",
            "Áudio  -  Síntese de ondas em tempo real",
            "",
            "Obrigado por jogar!",
        ]
        for i, ln in enumerate(lines):
            draw_text(surface, self.game.fonts["small"], ln, (cx, 230 + i * 46),
                      S.C_GOLD if i == 0 else S.C_WHITE, center=True)
        draw_text(surface, self.game.fonts["tiny"], "Pressione qualquer tecla para voltar",
                  (cx, 660), S.C_GREY, center=True)


class LevelSelectState(State):
    def on_enter(self, **kwargs):
        self.t = 0.0
        self.buttons = []
        unlocked = self.game.save.get("unlocked", 1)
        cx = S.SCREEN_WIDTH // 2
        f = self.game.fonts["medium"]
        for i, cfg in enumerate(S.LEVELS):
            lvl = cfg["id"]
            bx = cx - 330 + (i % 5) * 165
            b = Button(f"{lvl}", (bx, 360), size=(130, 130), font=self.game.fonts["large"])
            b.level_id = lvl
            b.locked = lvl > unlocked
            self.buttons.append(b)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state("menu")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in self.buttons:
                if b.rect.collidepoint(event.pos) and not b.locked:
                    self.game.sounds["select"].play()
                    self.game.change_state("gameplay", level_id=b.level_id)

    def update(self, dt):
        self.t += dt
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse)

    def draw(self, surface):
        draw_background(surface, self.t)
        cx = S.SCREEN_WIDTH // 2
        draw_text(surface, self.game.fonts["large"], "SELEÇÃO DE FASE", (cx, 140), S.C_HUD_ACCENT, center=True)
        for b in self.buttons:
            cfg = S.LEVELS[b.level_id - 1]
            b.draw(surface)
            if b.locked:
                overlay = pygame.Surface(b.rect.size, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                surface.blit(overlay, b.rect.topleft)
                draw_text(surface, self.game.fonts["medium"], "X",
                          b.rect.center, S.C_GREY, center=True)
            label = "CHEFÃO" if cfg.get("boss") else f"{cfg['goal']} maças"
            draw_text(surface, self.game.fonts["tiny"], label,
                      (b.rect.centerx, b.rect.bottom + 24), S.C_WHITE, center=True)
        draw_text(surface, self.game.fonts["tiny"], "ESC para voltar  -  Clique numa fase",
                  (cx, 640), S.C_GREY, center=True)
        hs = self.game.save.get("highscore", 0)
        draw_text(surface, self.game.fonts["small"], f"Recorde: {hs}", (cx, 560), S.C_GOLD, center=True)


class GameplayState(State):
    def on_enter(self, level_id=1, **kwargs):
        self.level_id = level_id
        self.cfg = S.LEVELS[level_id - 1]
        self.is_boss = self.cfg.get("boss", False)

        self.particles = ParticleSystem()
        self.flash = ScreenFlash()
        self.hud = HUD(self.game.fonts)

        self.walls = build_level(self.cfg)
        spawn = safe_spawn(self.walls)
        self.snake = Snake(spawn, self.game.sounds, self.particles)

        self.items = []
        self.apple = None
        self.apples = 0
        self.goal = self.cfg.get("goal", 0)
        self.goal_text = "∞" if self.is_boss else str(self.goal)

        self.special_timer = 4.0
        self.phase = "playing"
        self.phase_timer = 0.0
        self.t = 0.0

        self.predators = []
        if not self.is_boss and level_id >= 2:
            for _ in range(1 if level_id < 4 else 2):
                self.predators.append(Predator(self._far_point(spawn)))

        self.boss = None
        if self.is_boss:
            self.boss = Boss()
            self.game.play_music("boss")
        else:
            self.game.play_music("gameplay")

        self._spawn_apple()

    def _far_point(self, origin):
        x, y, w, h = S.ARENA_RECT
        for _ in range(100):
            p = random_arena_point(60)
            if (p - origin).length() > 280 and not self._blocked(p, 30):
                return p
        return pygame.Vector2(x + w - 120, y + 120)

    def _blocked(self, point, radius):
        for wall in self.walls:
            if wall.collides_circle(point, radius):
                return True
        return False

    def _spawn_apple(self):
        for _ in range(200):
            p = random_arena_point(50)
            if not self._blocked(p, 30) and (p - self.snake.head).length() > 120:
                self.apple = Item("apple", p)
                return
        self.apple = Item("apple", random_arena_point(50))

    def _spawn_special(self):
        special_count = len([i for i in self.items])
        if special_count >= self.cfg.get("max_items", 1):
            return
        kind = pick_special_kind()
        if kind is None:
            return
        for _ in range(60):
            p = random_arena_point(50)
            if not self._blocked(p, 30) and (p - self.snake.head).length() > 120:
                self.items.append(Item(kind, p))
                return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.phase == "playing":
                    self.phase = "paused"
                elif self.phase == "paused":
                    self.phase = "playing"
            elif event.key == pygame.K_m and self.phase == "paused":
                self.game.change_state("menu")
            elif event.key == pygame.K_SPACE and self.phase == "playing":
                self.snake.try_dash()

    def _read_input(self):
        keys = pygame.key.get_pressed()
        v = pygame.Vector2()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            v.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            v.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            v.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            v.x += 1
        self.snake.set_input_direction(v)

    def update(self, dt):
        self.t += dt
        self.flash.update(dt)
        self.particles.update(dt)

        if self.phase == "paused":
            return

        if self.phase == "complete":
            self.phase_timer -= dt
            if self.phase_timer <= 0:
                self._advance_level()
            return

        if self.phase == "victory_wait":
            self.phase_timer -= dt
            self.particles.update(dt)
            if self.phase_timer <= 0:
                self.game.change_state("victory", level_id=self.level_id)
            return

        self._read_input()
        self.snake.update(dt)

        for wall in self.walls:
            wall.update(dt)

        if self.apple:
            self.apple.update(dt)
        for it in self.items:
            it.update(dt)

        self.special_timer -= dt
        if self.special_timer <= 0:
            self.special_timer = random.uniform(6, 11)
            self._spawn_special()

        self._handle_item_pickup()

        for pred in self.predators:
            pred.update(dt, self.snake.head, self.walls)

        if self.boss:
            self._update_boss(dt)

        self._handle_collisions()

        self.hud.update(self.snake, dt, self.boss)

        if not self.is_boss and self.apples >= self.goal:
            self._complete_level()

    def _update_boss(self, dt):
        self.boss.update(dt, self.snake, self.particles)
        if self.boss.sound_request:
            req = self.boss.sound_request
            self.boss.sound_request = None
            if req == "boss_attack":
                self.game.sounds["boss_attack"].play()
            elif req == "hit":
                self.game.sounds["hit"].play()
            elif req == "boss_dead":
                self.game.sounds["victory"].play()

        if self.boss.exploded:
            self.phase = "victory_wait"
            self.phase_timer = 1.2
            self.game.save["highscore"] = max(self.game.save.get("highscore", 0), self.snake.score)
            self.game.save["unlocked"] = max(self.game.save.get("unlocked", 1), 5)
            self.game.write_save()
            return

        if self.snake.invulnerable <= 0 and not self.snake.ghost_mode:
            if self.boss.check_weak_hit(self.snake, self.particles):
                self.snake.score += 100
            elif self.boss.check_projectile_hits(self.snake):
                self._damage_snake()
            elif self.boss.check_charge_hit(self.snake):
                self._damage_snake()
        else:
            self.boss.check_weak_hit(self.snake, self.particles)

    def _handle_item_pickup(self):
        if self.apple and self.apple.collides_with(self.snake.head, self.snake.radius):
            self.snake.grow(1)
            self.snake.score += 10
            self.apples += 1
            self.game.sounds["eat"].play()
            self.particles.burst(self.apple.pos, S.C_APPLE, count=18, speed=200)
            self._spawn_apple()

        remaining = []
        for it in self.items:
            if it.collides_with(self.snake.head, self.snake.radius):
                self.snake.apply_effect(it.kind)
                self.particles.burst(it.pos, it.color, count=20, speed=200)
            else:
                remaining.append(it)
        self.items = remaining

    def _handle_collisions(self):
        if self.snake.ghost_mode or self.snake.invulnerable > 0:
            return

        if self.snake.hits_arena_bounds():
            self._damage_snake()
            return

        for wall in self.walls + (self.boss.all_collision_walls() if self.boss else []):
            if wall.collides_circle(self.snake.head, self.snake.radius):
                self._damage_snake()
                return

        if self.snake.self_collision():
            self._damage_snake()
            return

        for pred in self.predators:
            if pred.caught(self.snake.head, self.snake.radius):
                self._damage_snake()
                return

    def _damage_snake(self):
        self.snake.lose_life()
        self.flash.trigger((255, 60, 60), 0.35)
        self.particles.burst(self.snake.head, (255, 80, 80), count=24, speed=220)
        if self.snake.lives <= 0:
            self.game.save["highscore"] = max(self.game.save.get("highscore", 0), self.snake.score)
            self.game.write_save()
            self.game.sounds["gameover"].play()
            self.game.change_state("defeat", level_id=self.level_id)
        else:
            spawn = safe_spawn(self.walls)
            self.snake.respawn(spawn)

    def _complete_level(self):
        self.phase = "complete"
        self.phase_timer = 2.0
        self.game.sounds["victory"].play()
        unlocked = self.game.save.get("unlocked", 1)
        self.game.save["unlocked"] = max(unlocked, min(len(S.LEVELS), self.level_id + 1))
        self.game.save["highscore"] = max(self.game.save.get("highscore", 0), self.snake.score)
        self.game.write_save()

    def _advance_level(self):
        if self.level_id < len(S.LEVELS):
            self.game.change_state("gameplay", level_id=self.level_id + 1)
        else:
            self.game.change_state("victory", level_id=self.level_id)

    def draw(self, surface):
        surface.fill(S.C_BG)
        ax, ay, aw, ah = S.ARENA_RECT
        pygame.draw.rect(surface, S.C_ARENA, (ax, ay, aw, ah), border_radius=8)
        for gx in range(ax, ax + aw, 48):
            pygame.draw.line(surface, S.C_ARENA_LINE, (gx, ay), (gx, ay + ah))
        for gy in range(ay, ay + ah, 48):
            pygame.draw.line(surface, S.C_ARENA_LINE, (ax, gy), (ax + aw, gy))
        pygame.draw.rect(surface, S.C_HUD_ACCENT, (ax, ay, aw, ah), 3, border_radius=8)

        for wall in self.walls:
            wall.draw(surface)

        if self.apple:
            self.apple.draw(surface)
        for it in self.items:
            it.draw(surface)

        for pred in self.predators:
            pred.draw(surface)

        if self.boss:
            self.boss.draw(surface)

        self.snake.draw(surface)
        self.particles.draw(surface)
        self.flash.draw(surface)

        self.hud.draw(surface, self.snake, self)

        if self.phase == "complete":
            self._overlay(surface, "FASE COMPLETA", S.C_SNAKE)
        elif self.phase == "victory_wait":
            self._overlay(surface, "CHEFÃO DERROTADO", S.C_GOLD)
        elif self.phase == "paused":
            self._overlay(surface, "PAUSADO", S.C_HUD_ACCENT,
                          sub="ESC para continuar  -  M para menu")

    def _overlay(self, surface, text, color, sub=None):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        cx, cy = S.SCREEN_WIDTH // 2, S.SCREEN_HEIGHT // 2
        scale = 1.0 + 0.05 * math.sin(self.t * 6)
        draw_text(surface, self.game.fonts["large"], text, (cx, cy), color, center=True)
        if sub:
            draw_text(surface, self.game.fonts["small"], sub, (cx, cy + 70), S.C_WHITE, center=True)


class VictoryState(State):
    def on_enter(self, level_id=1, **kwargs):
        self.t = 0.0
        self.particles = ParticleSystem()
        self.game.play_music("menu")
        self.game.sounds["victory"].play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_state("menu")

    def update(self, dt):
        self.t += dt
        if random.random() < 0.3:
            p = (random.randint(0, S.SCREEN_WIDTH), random.randint(100, 400))
            self.particles.burst(p, random.choice([S.C_GOLD, S.C_SNAKE, S.C_HUD_ACCENT]),
                                 count=14, speed=200)
        self.particles.update(dt)

    def draw(self, surface):
        draw_background(surface, self.t)
        self.particles.draw(surface)
        cx = S.SCREEN_WIDTH // 2
        bob = math.sin(self.t * 3) * 8
        draw_text(surface, self.game.fonts["title"], "VITÓRIA!", (cx, 260 + bob), S.C_GOLD, center=True)
        draw_text(surface, self.game.fonts["medium"],
                  "Você completou Cobralia: Snake Ascension", (cx, 360), S.C_WHITE, center=True)
        draw_text(surface, self.game.fonts["small"],
                  f"Recorde: {self.game.save.get('highscore', 0)}", (cx, 430), S.C_HUD_ACCENT, center=True)
        draw_text(surface, self.game.fonts["tiny"],
                  "Pressione qualquer tecla para voltar ao menu", (cx, 600), S.C_GREY, center=True)


class DefeatState(State):
    def on_enter(self, level_id=1, **kwargs):
        self.t = 0.0
        self.level_id = level_id
        self.game.play_music("menu")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.change_state("gameplay", level_id=self.level_id)
            else:
                self.game.change_state("menu")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_state("menu")

    def update(self, dt):
        self.t += dt

    def draw(self, surface):
        draw_background(surface, self.t)
        cx = S.SCREEN_WIDTH // 2
        draw_text(surface, self.game.fonts["title"], "GAME OVER", (cx, 260), S.C_APPLE, center=True)
        draw_text(surface, self.game.fonts["small"],
                  f"Você caiu na fase {self.level_id}", (cx, 360), S.C_WHITE, center=True)
        draw_text(surface, self.game.fonts["medium"],
                  "ENTER para tentar de novo", (cx, 440), S.C_HUD_ACCENT, center=True)
        draw_text(surface, self.game.fonts["tiny"],
                  "Qualquer outra tecla volta ao menu", (cx, 600), S.C_GREY, center=True)
