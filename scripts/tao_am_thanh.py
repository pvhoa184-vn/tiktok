"""Tự tổng hợp nhạc nền và hiệu ứng âm thanh (không bản quyền) cho video.

Cách dùng:
    python scripts/tao_am_thanh.py --out assets/sfx            # tạo bộ SFX
    python scripts/tao_am_thanh.py --nhac 30 --bpm 108 --out assets/nhac/beat.wav
Cần: numpy, scipy.
"""
import argparse
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100


def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
    return e


def lp(x, f):
    b, a = butter(2, f / (SR / 2), "low")
    return lfilter(b, a, x)


def hp(x, f):
    b, a = butter(2, f / (SR / 2), "high")
    return lfilter(b, a, x)


def kick(d=0.35):
    n = int(SR * d); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)


def clap(d=0.25):
    n = int(SR * d)
    return hp(np.random.randn(n), 900) * env(n, 0.001, 0.06) * 0.6


def hat(d=0.06):
    n = int(SR * d)
    return hp(np.random.randn(n), 7000) * env(n, 0.001, 0.015) * 0.35


def note(freq, d, wave="saw", r=0.3):
    n = int(SR * d); t = np.arange(n) / SR
    if wave == "saw":
        x = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, 8))
    else:
        x = np.sin(2 * np.pi * freq * t)
    return x * env(n, 0.01, r)


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def nhac(sec, bpm):
    beat = 60 / bpm; n = int(SR * sec); out = np.zeros(n + SR * 2)
    def put(x, t, g=1.0):
        i = int(t * SR); out[i:i + len(x)] += x[: len(out) - i] * g
    # vòng hợp âm Am - F - C - G (mỗi hợp âm 1 ô nhịp)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    bass = [45, 41, 48, 43]
    bars = int(sec / (beat * 4)) + 1
    for b in range(bars):
        t0 = b * beat * 4
        ch = chords[b % 4]
        for m in ch:
            put(lp(note(midi(m), beat * 4, "saw", 1.2), 1800), t0, 0.05)
        for i in range(8):  # bass móc 8 nốt
            put(lp(note(midi(bass[b % 4]), beat / 2, "saw", 0.12), 600), t0 + i * beat / 2, 0.16)
        for i in range(8):  # arpeggio
            m = ch[[0, 1, 2, 1][i % 4]] + 12
            put(lp(note(midi(m), beat / 2, "sine", 0.12), 4000), t0 + i * beat / 2, 0.07)
        for i in range(4):
            put(kick(), t0 + i * beat, 0.9)
            if i in (1, 3):
                put(clap(), t0 + i * beat, 0.5)
        for i in range(8):
            put(hat(), t0 + i * beat / 2 + (beat / 4 if i % 2 else 0) * 0, 0.6 if i % 2 else 0.3)
    out = out[:n]
    fade = int(SR * 1.5); out[-fade:] *= np.linspace(1, 0, fade)
    out[: int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
    return out / (np.abs(out).max() + 1e-9) * 0.8


def sfx():
    s = {}
    n = int(SR * 0.12); t = np.arange(n) / SR  # pop
    s["pop"] = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 25) + 300) / SR) * env(n, 0.001, 0.03)
    n = int(SR * 0.9); t = np.arange(n) / SR  # ding
    s["ding"] = sum(np.sin(2 * np.pi * f * t) * g for f, g in [(1318, 1), (2637, .4), (3951, .15)]) * env(n, 0.002, 0.25) * 0.6
    n = int(SR * 0.5); t = np.arange(n) / SR  # whoosh: nhiễu quét tần số
    noise = np.random.randn(n); w = np.zeros(n); step = 512
    for i in range(0, n, step):
        f = 300 + 5000 * (i / n)
        w[i:i + step] = lp(noise[i:i + step], min(f, 15000))
    s["whoosh"] = w * np.sin(np.pi * t / t[-1]) * 0.7
    n = int(SR * 0.8); t = np.arange(n) / SR  # boom
    s["boom"] = (np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-t * 12)) / SR) * env(n, 0.001, 0.3)
                 + lp(np.random.randn(n), 400) * env(n, 0.001, 0.08) * 0.5)
    n = int(SR * 0.08); t = np.arange(n) / SR  # tick
    s["tick"] = np.sin(2 * np.pi * 2200 * t) * env(n, 0.0005, 0.012) * 0.7
    return s


def save(x, p):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    wavfile.write(p, SR, (x * 32767).astype(np.int16))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nhac", type=float, help="độ dài nhạc nền (giây)")
    ap.add_argument("--bpm", type=float, default=108)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    np.random.seed(7)
    if a.nhac:
        save(nhac(a.nhac, a.bpm), a.out)
    else:
        for k, v in sfx().items():
            save(v, Path(a.out) / f"{k}.wav")
    print("xong:", a.out)
