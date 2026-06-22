import os
import sys
import json
import pygame

import settings as S


def ensure_asset_dirs():
    for sub in ("sprites", "sounds", "music", "fonts"):
        os.makedirs(os.path.join(S.ASSETS_DIR, sub), exist_ok=True)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        try:
            pygame.mixer.init()
            self.audio_ok = True
        except pygame.error:
            self.audio_ok = False

        ensure_asset_dirs()

        self.screen = pygame.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.fonts = self._load_fonts()
        self.sounds = self._load_sounds()
        self.music_tracks = self._load_music()

        self.music_channel = pygame.mixer.Channel(0) if self.audio_ok else None
        self.current_music = None

        self.save = self._load_save()

        from states import (MenuState, ControlsState, CreditsState,
                            LevelSelectState, GameplayState, VictoryState, DefeatState)
        self.states = {
            "menu": MenuState(self),
            "controls": ControlsState(self),
            "credits": CreditsState(self),
            "levelselect": LevelSelectState(self),
            "gameplay": GameplayState(self),
            "victory": VictoryState(self),
            "defeat": DefeatState(self),
        }
        self.state = None
        self.change_state("menu")

    def _load_fonts(self):
        def f(size, bold=False):
            try:
                return pygame.font.SysFont("consolas,couriernew,arial", size, bold=bold)
            except Exception:
                return pygame.font.Font(None, size)
        return {
            "title": f(96, True),
            "large": f(56, True),
            "medium": f(38, True),
            "small": f(26),
            "tiny": f(20),
        }

    def _silent(self):
        class _Null:
            def play(self, *a, **k):
                return None
            def stop(self, *a, **k):
                return None
        return _Null()

    def _load_sounds(self):
        if not self.audio_ok:
            keys = ["eat", "dash", "powerup", "powerdown", "hurt", "boss_attack",
                    "victory", "gameover", "select", "hit"]
            return {k: self._silent() for k in keys}
        import audio
        try:
            return audio.build_sounds()
        except Exception:
            keys = ["eat", "dash", "powerup", "powerdown", "hurt", "boss_attack",
                    "victory", "gameover", "select", "hit"]
            return {k: self._silent() for k in keys}

    def _load_music(self):
        if not self.audio_ok:
            return {}
        import audio
        try:
            return audio.build_music()
        except Exception:
            return {}

    def play_music(self, name):
        if not self.audio_ok or self.music_channel is None:
            return
        if self.current_music == name:
            return
        track = self.music_tracks.get(name)
        if track is None:
            return
        self.music_channel.stop()
        self.music_channel.set_volume(0.5)
        self.music_channel.play(track, loops=-1)
        self.current_music = name

    def _load_save(self):
        default = {"unlocked": 1, "highscore": 0}
        try:
            if os.path.exists(S.SAVE_FILE):
                with open(S.SAVE_FILE, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                default.update({k: data.get(k, default[k]) for k in default})
        except Exception:
            pass
        return default

    def write_save(self):
        try:
            with open(S.SAVE_FILE, "w", encoding="utf-8") as fh:
                json.dump(self.save, fh, indent=2)
        except Exception:
            pass

    def change_state(self, name, **kwargs):
        self.state = self.states[name]
        self.state.on_enter(**kwargs)

    def run(self):
        while self.running:
            dt = self.clock.tick(S.FPS) / 1000.0
            dt = min(dt, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()

        self.write_save()
        pygame.quit()
        sys.exit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
