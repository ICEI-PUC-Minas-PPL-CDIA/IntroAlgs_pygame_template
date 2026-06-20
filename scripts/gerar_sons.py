
import math
import struct
import subprocess
import sys
from pathlib import Path

SAMPLE_RATE = 44100
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "sons"


def _tone(freq, duration, volume=0.35, fade_out=True):
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        env = max(0.0, 1.0 - (i / n)) if fade_out else 1.0
        val = volume * env * math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out


def _noise(duration, volume=0.3):
    n = int(SAMPLE_RATE * duration)
    out, x = [], 12345
    for i in range(n):
        x = (1103515245 * x + 12345) & 0x7FFFFFFF
        env = max(0.0, 1.0 - (i / n))
        val = volume * env * ((x / 0x7FFFFFFF) * 2 - 1)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out


def _sweep(f0, f1, duration, volume=0.3):
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        f = f0 + (f1 - f0) * (i / max(1, n - 1))
        env = max(0.0, 1.0 - (i / n) * 0.5)
        val = volume * env * math.sin(2 * math.pi * f * (i / SAMPLE_RATE))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out


def _ambient_loop(duration=8.0):
    n = int(SAMPLE_RATE * duration)
    out = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = sum(0.07 * math.sin(2 * math.pi * f * t + p) for f, p in ((110, 0), (165, 1.2), (220, 2.1), (330, 0.5)))
        val += 0.03 * math.sin(2 * math.pi * 0.2 * t)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out


def _write_wav(path, samples):
    import wave

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))


def _wav_to_ogg(wav_path, ogg_path):
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path), str(ogg_path)],
            check=True,
            capture_output=True,
        )
        wav_path.unlink(missing_ok=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _emit(name, samples):
    wav_path = OUT_DIR / name.replace(".ogg", ".wav")
    ogg_path = OUT_DIR / name
    _write_wav(wav_path, samples)
    if _wav_to_ogg(wav_path, ogg_path):
        print(f"Gerado: {ogg_path} ({ogg_path.stat().st_size} bytes)")
    else:
        final = OUT_DIR / name.replace(".ogg", ".wav")
        if wav_path != final:
            wav_path.rename(final)
        print(f"Gerado: {final} ({final.stat().st_size} bytes) [ffmpeg ausente — use .wav]")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    _emit("colisao.ogg", _noise(0.3, 0.45) + _tone(90, 0.2, 0.4))
    _emit("level_up.ogg", _sweep(320, 880, 0.4))
    _emit("game_over.ogg", _sweep(420, 100, 0.9))
    _emit("musica.ogg", _ambient_loop())


if __name__ == "__main__":
    main()
