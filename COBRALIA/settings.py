import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Cobralia: Snake Ascension"

ARENA_MARGIN = 40
ARENA_RECT = (ARENA_MARGIN, ARENA_MARGIN + 60,
              SCREEN_WIDTH - ARENA_MARGIN * 2,
              SCREEN_HEIGHT - ARENA_MARGIN * 2 - 60)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SAVE_FILE = os.path.join(BASE_DIR, "savegame.json")

C_BG = (12, 14, 24)
C_BG2 = (18, 22, 38)
C_ARENA = (22, 26, 44)
C_ARENA_LINE = (40, 48, 80)
C_WHITE = (236, 240, 255)
C_GREY = (120, 130, 160)
C_DARKGREY = (60, 66, 92)
C_SNAKE = (80, 220, 120)
C_SNAKE_DARK = (40, 150, 80)
C_SNAKE_HEAD = (150, 255, 180)
C_GHOST = (140, 200, 255)
C_APPLE = (235, 70, 70)
C_PEPPER = (255, 140, 30)
C_ICE = (120, 200, 255)
C_MUSHROOM = (190, 90, 220)
C_SCISSORS = (220, 220, 120)
C_GHOST_ITEM = (200, 220, 255)
C_WALL = (90, 100, 140)
C_WALL_MOVING = (210, 120, 60)
C_PREDATOR = (230, 60, 90)
C_BOSS = (160, 170, 200)
C_BOSS_WEAK = (255, 60, 60)
C_BOSS_WEAK_OPEN = (255, 200, 60)
C_HUD = (28, 32, 52)
C_HUD_ACCENT = (90, 200, 255)
C_HP = (235, 70, 70)
C_DASH_READY = (90, 220, 255)
C_GOLD = (255, 210, 90)

SNAKE_SPEED_INITIAL = 180.0
SNAKE_SPEED_MAX = 350.0
DASH_SPEED = 500.0
PREDATOR_SPEED = 220.0

SEGMENT_RADIUS = 9
SEGMENT_SPACING = 13
HEAD_RADIUS = 12
START_SEGMENTS = 5
START_LIVES = 3

DASH_DURATION = 0.3
DASH_COOLDOWN = 3.0
DASH_COST_SEGMENTS = 1
DASH_COST_POINTS = 5

PEPPER_DURATION = 10.0
ICE_DURATION = 10.0
MUSHROOM_DURATION = 8.0
GHOST_DURATION = 7.0
SCISSORS_CUT = 3

PEPPER_MULT = 1.5
ICE_MULT = 0.5

PREDATOR_DETECT_RADIUS = 250.0

SPECIAL_ITEM_CHANCE = {
    "pepper": 0.20,
    "ice": 0.18,
    "mushroom": 0.15,
    "scissors": 0.15,
    "ghost": 0.12,
}

BOSS_MAX_HP = 3
BOSS_WEAK_OPEN_TIME = 2.0
BOSS_WEAK_CLOSED_TIME = 4.0

LEVELS = [
    {"id": 1, "goal": 5, "moving_walls": 0, "max_items": 1},
    {"id": 2, "goal": 10, "moving_walls": 2, "max_items": 2},
    {"id": 3, "goal": 15, "moving_walls": 3, "max_items": 2},
    {"id": 4, "goal": 20, "moving_walls": 4, "max_items": 3},
    {"id": 5, "goal": 0, "moving_walls": 0, "max_items": 1, "boss": True},
]
