import math
import array
import pygame

SAMPLE_RATE = 44100


def _clamp(v):
    if v > 32767:
        return 32767
    if v < -32768:
        return -32768
    return int(v)


def _make_sound(samples):
    buf = array.array("h")
    for s in samples:
        v = _clamp(s * 32767)
        buf.append(v)
        buf.append(v)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def _tone(freq, duration, volume=0.5, wave="sine", decay=True):
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        phase = 2 * math.pi * freq * t
        if wave == "sine":
            val = math.sin(phase)
        elif wave == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave == "saw":
            val = 2.0 * (t * freq - math.floor(0.5 + t * freq))
        else:
            val = math.sin(phase)
        env = 1.0
        if decay:
            env = max(0.0, 1.0 - (i / n))
        out.append(val * volume * env)
    return out


def _sweep(f0, f1, duration, volume=0.5, wave="sine"):
    n = int(SAMPLE_RATE * duration)
    out = []
    phase = 0.0
    for i in range(n):
        frac = i / n
        freq = f0 + (f1 - f0) * frac
        phase += 2 * math.pi * freq / SAMPLE_RATE
        if wave == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave == "saw":
            val = 2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0
        else:
            val = math.sin(phase)
        env = max(0.0, 1.0 - frac)
        out.append(val * volume * env)
    return out


def _noise_burst(duration, volume=0.5):
    import random
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        env = max(0.0, 1.0 - (i / n))
        out.append((random.random() * 2 - 1) * volume * env)
    return out


def _mix(*tracks):
    length = max(len(t) for t in tracks)
    out = [0.0] * length
    for t in tracks:
        for i, v in enumerate(t):
            out[i] += v
    return out


def build_sounds():
    sounds = {}
    sounds["eat"] = _make_sound(_sweep(440, 880, 0.12, 0.5, "sine"))
    sounds["dash"] = _make_sound(_sweep(200, 700, 0.25, 0.45, "saw"))
    sounds["powerup"] = _make_sound(_mix(_tone(523, 0.10, 0.3),
                                         _tone(659, 0.10, 0.3),
                                         _tone(784, 0.14, 0.3)))
    sounds["powerdown"] = _make_sound(_sweep(500, 120, 0.30, 0.4, "saw"))
    sounds["hurt"] = _make_sound(_mix(_sweep(300, 60, 0.30, 0.5, "square"),
                                      _noise_burst(0.15, 0.2)))
    sounds["boss_attack"] = _make_sound(_sweep(160, 420, 0.20, 0.5, "square"))
    sounds["victory"] = _make_sound(_mix(_tone(523, 0.5, 0.25),
                                         _tone(659, 0.5, 0.25),
                                         _tone(784, 0.5, 0.25)))
    sounds["gameover"] = _make_sound(_sweep(400, 80, 0.7, 0.45, "saw"))
    sounds["select"] = _make_sound(_tone(660, 0.06, 0.35, "square"))
    sounds["hit"] = _make_sound(_mix(_tone(880, 0.10, 0.4), _noise_burst(0.08, 0.2)))
    return sounds


def _melody(notes, base_volume=0.18, wave="square"):
    out = []
    for freq, dur in notes:
        if freq <= 0:
            out.extend([0.0] * int(SAMPLE_RATE * dur))
        else:
            out.extend(_tone(freq, dur, base_volume, wave, decay=False))
    return out


def build_music():
    music = {}
    menu_notes = [(330, 0.3), (392, 0.3), (494, 0.3), (392, 0.3),
                  (440, 0.3), (392, 0.3), (330, 0.3), (0, 0.3)]
    music["menu"] = _make_sound(_melody(menu_notes, 0.14, "sine"))

    play_notes = [(262, 0.2), (330, 0.2), (392, 0.2), (523, 0.2),
                  (392, 0.2), (330, 0.2), (294, 0.2), (349, 0.2)]
    music["gameplay"] = _make_sound(_melody(play_notes, 0.13, "square"))

    boss_notes = [(196, 0.18), (196, 0.18), (233, 0.18), (196, 0.18),
                  (175, 0.18), (196, 0.18), (147, 0.18), (196, 0.18)]
    music["boss"] = _make_sound(_melody(boss_notes, 0.15, "saw"))
    return music
