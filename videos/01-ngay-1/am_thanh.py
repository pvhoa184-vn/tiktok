"""Tạo nền âm thanh cho video Ngày 1/90 rồi trộn với hình đã render.

Cách dùng (chạy trong thư mục videos/01-ngay-1):
    python am_thanh.py                 # tạo renders/nen.wav và renders/final.mp4
Giọng: tạo bằng tao_giong_ngay1.py (VieNeu, ra giong/*.raw.wav), hoặc thu thật rồi ghi đè đúng tên trong GIONG.
Thiếu file nào thì bỏ qua câu đó, video vẫn chạy bằng chữ trong bong bóng.
Cần: numpy, scipy, ffmpeg.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from tao_am_thanh import SR, clap, env, hat, hp, kick, lp, midi, nhac, note, sfx  # noqa: E402

DAI = 28.6
CAT_NHAC = 13.2      # nhạc tắt đột ngột, lúc anh cơ bắp tới chỉnh tạ
NHAC_NHE = 17.2      # nhạc vào lại nhẹ
NHAC_LEN = 20.6      # nhạc lên lại
UC = 26.2            # tiếng "ực"

# Giọng: (file trong giong/, giây bắt đầu, kiểu). Khớp với bong bóng trong index.html.
# Tạo bằng tao_giong_ngay1.py (VieNeu). Thu giọng thật thì ghi đè đúng tên file là xong.
GIONG = [
    ("1-muoi-phut.raw.wav", 2.6, "be-dau"),   # Mười phút rồi. Vẫn chưa dám vào.
    ("2-gia-vo.raw.wav", 5.3, "be-dau"),      # Giả vờ nghe điện thoại. Không ai gọi cả.
    ("3-cam-vay.raw.wav", 8.2, "be-dau"),     # Cầm vậy là đúng chưa ta?
    ("4-thoi-xong.raw.wav", 10.6, "be-dau"),  # Thôi xong. Ảnh đi về phía mình.
    ("co-bap.raw.wav", 13.6, "co-bap"),       # Cầm thế này nè. Hồi đầu anh cũng cầm ngược.
]
# Bé Đậu nói trong đầu: bớt trầm, hơi vang như tiếng nghĩ. Anh cơ bắp: tiếng phòng thật.
LOC = {
    "be-dau": "highpass=f=140,lowpass=f=7500,aecho=0.8:0.5:40:0.1,volume=4dB",
    "co-bap": "highpass=f=80,volume=5dB",
}


def nhac_cang(sec, bpm=96):
    """Nhạc hồi hộp: tiếng tim đập, tích tắc, nốt trầm kéo dài, dày dần."""
    beat = 60 / bpm
    n = int(SR * sec)
    out = np.zeros(n + SR * 2)

    def put(x, t, g=1.0):
        i = int(t * SR)
        out[i:i + len(x)] += x[: len(out) - i] * g

    bars = int(sec / (beat * 4)) + 1
    for b in range(bars):
        t0 = b * beat * 4
        up = min(1.0, 0.45 + b * 0.12)          # dày dần
        root = [45, 45, 46, 44][b % 4]          # A A Bb G#: lệch nửa cung cho căng
        put(lp(note(midi(root - 12), beat * 4, "saw", 2.0), 260), t0, 0.22 * up)
        put(lp(note(midi(root + 15), beat * 4, "saw", 1.6), 1400), t0, 0.035 * up)
        for i in range(4):                       # tim đập: thình-thịch mỗi phách
            put(kick(0.25), t0 + i * beat, 0.7 * up)
            put(kick(0.2), t0 + i * beat + 0.16, 0.4 * up)
        for i in range(8):                       # tích tắc
            put(hat(0.04), t0 + i * beat / 2, 0.5 if i % 2 else 0.25)
        if b >= 2:
            for i in range(16):
                put(hat(0.03), t0 + i * beat / 4, 0.12 * up)
    out = out[:n]
    out[: int(SR * 0.2)] *= np.linspace(0, 1, int(SR * 0.2))
    return out / (np.abs(out).max() + 1e-9) * 0.8


def scratch():
    """Tiếng rít đĩa than khi nhạc tắt."""
    d = 0.35
    m = int(SR * d)
    t = np.arange(m) / SR
    f = 900 * np.exp(-t * 6) + 120
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + hp(np.random.randn(m), 1500) * 0.35
    return x * env(m, 0.002, 0.12)


def uc():
    """Tiếng nuốt nước bọt: tiếng 'ực' trầm, ướt."""
    m = int(SR * 0.32)
    t = np.arange(m) / SR
    f = 240 * np.exp(-t * 9) + 70
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(m, 0.004, 0.07)
    click = hp(np.random.randn(m), 2500) * env(m, 0.0005, 0.006) * 0.6
    wet = lp(np.random.randn(m), 700) * env(m, 0.01, 0.05) * 0.5
    return tone + click + wet


def room(sec):
    """Tiếng phòng rất nhỏ khi nhạc tắt, để im lặng không giống lỗi mất tiếng."""
    m = int(SR * sec)
    return lp(np.random.randn(m), 500) * 0.02


def main():
    np.random.seed(11)
    n = int(SR * DAI)
    bed = np.zeros(n + SR)

    def put(x, t, g=1.0):
        i = int(t * SR)
        bed[i:i + len(x)] += x[: len(bed) - i] * g

    # 1. nhạc căng tới 13.4 rồi tắt phụt
    c = nhac_cang(CAT_NHAC + 0.05)
    c[-int(SR * 0.01):] *= np.linspace(1, 0, int(SR * 0.01))
    put(c, 0, 0.55)
    put(scratch(), CAT_NHAC - 0.05, 0.55)
    put(room(NHAC_NHE - CAT_NHAC), CAT_NHAC + 0.3)

    # 2. nhạc vui: vào nhẹ (lọc trầm, như nghe qua tường) rồi lên hẳn khi đeo tai nghe
    vui = nhac(DAI - NHAC_NHE + 0.5, 108)
    soft = lp(vui[: int(SR * (NHAC_LEN - NHAC_NHE))], 700)
    soft *= np.linspace(0, 1, len(soft)) ** 1.5
    put(soft, NHAC_NHE, 0.35)
    full = vui[int(SR * (NHAC_LEN - NHAC_NHE)):].copy()
    du = np.ones(len(full))                     # hạ nhạc lúc "ực"
    i0, i1 = int(SR * (UC - 0.15 - NHAC_LEN)), int(SR * (UC + 0.6 - NHAC_LEN))
    du[i0:i1] = 0.35
    du = np.convolve(du, np.ones(2000) / 2000, mode="same")
    put(full * du, NHAC_LEN, 0.85)

    # 3. SFX
    s = sfx()
    for t in (2.4, 8.0, 10.4, 20.6, 24.6):
        put(s["whoosh"], t - 0.15, 0.35)
    for t in (2.5, 5.2, 8.1, 10.5):            # bong bóng suy nghĩ
        put(s["pop"], t, 0.25)
    for i in range(5):                          # bước chân anh cơ bắp, dồn dần
        put(kick(0.3), 10.7 + i * 0.5, 0.25 + i * 0.08)
    put(s["pop"], 13.45, 0.2)                   # bong bóng lời anh cơ bắp
    put(s["ding"], 18.75, 0.25)                 # "Không biết thì cứ hỏi."
    put(s["boom"], 20.8, 0.5)
    put(s["ding"], 21.7, 0.3)
    put(uc(), UC, 0.9)

    bed = bed[:n]
    bed[-int(SR * 0.8):] *= np.linspace(1, 0, int(SR * 0.8))
    Path("renders").mkdir(exist_ok=True)
    wavfile.write("renders/nen.wav", SR, (bed / (np.abs(bed).max() + 1e-9) * 0.9 * 32767).astype(np.int16))

    # 4. trộn giọng (nếu có) + nền + hình
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", "renders/hinh.mp4", "-i", "renders/nen.wav"]
    parts, k = [], 0
    for f, t, kieu in GIONG:
        p = Path("giong") / f
        if p.exists():
            cmd += ["-i", str(p)]
            ms = int(t * 1000)
            parts.append(f"[{k + 2}]aresample=44100,aformat=channel_layouts=mono,{LOC[kieu]},adelay={ms}|{ms}[g{k}]")
            k += 1
    if k:
        mix = ";".join(parts) + ";" + "".join(f"[g{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0,apad=whole_dur={DAI},asplit=2[voc][voc2];"
        mix += "[1][voc]sidechaincompress=threshold=0.02:ratio=9:attack=15:release=300[duck];"
        mix += "[duck][voc2]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[out]"
    else:
        mix = "[1]loudnorm=I=-14:TP=-1.5:LRA=9[out]"
    cmd += ["-filter_complex", mix, "-map", "0:v", "-map", "[out]", "-c:v", "libx264", "-crf", "20",
            "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-t", str(DAI), "-movflags", "+faststart", "renders/final.mp4"]
    subprocess.run(cmd, check=True)
    print(f"xong: renders/final.mp4 ({k} file giọng)")


if __name__ == "__main__":
    main()
