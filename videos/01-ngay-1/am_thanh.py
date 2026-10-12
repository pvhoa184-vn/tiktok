"""Tạo nền âm thanh cho video Ngày 1/100 (bản 3) rồi trộn với hình đã render.

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
from tao_am_thanh import SR, env, hp, kick, lp, nhac, sfx  # noqa: E402

DAI = 32.4
VAO_MAY = 10.2       # cắt sang máy kéo xô: nhạc rõ hơn
NHO_LAI = 22.4       # anh tập lâu nói: nhạc nhỏ lại
LEN_LAI = 26.4       # hạ đệm xong: nhạc lên lại

# Giọng: (file trong giong/, giây bắt đầu, kiểu). Khớp với bong bóng trong index.html.
GIONG = [
    ("1-dem.raw.wav", 2.4, "be-dau"),        # Rồi. Đếm tới ba là vào. Một. Hai...
    ("2-khoan.raw.wav", 5.4, "be-dau"),      # Khoan. Uống miếng nước cái đã.
    ("3-bay-len.raw.wav", 10.7, "be-dau"),   # Ủa. Kéo xuống mà mình bay lên.
    ("4-hoi-thu.raw.wav", 15.15, "be-dau"),  # Chắc ảnh đợi máy. Thôi, hỏi thử.
    ("5-anh-oi.raw.wav", 18.05, "be-dau-noi"),  # Anh ơi, máy này chỉnh sao vậy anh? ...
    ("co-bap.raw.wav", 22.55, "co-bap"),     # Hạ cái đệm này xuống nè. ...
]
# Bé Đậu nói nhỏ một mình: hơi vang nhẹ. Nói ra tiếng với anh tập lâu và giọng anh: tiếng phòng thật.
LOC = {
    "be-dau": "highpass=f=120,lowpass=f=8000,aecho=0.8:0.3:30:0.08,volume=4dB",
    "be-dau-noi": "highpass=f=100,volume=4dB",
    "co-bap": "highpass=f=80,volume=5dB",
}


def uc():
    """Tiếng nuốt nước bọt: tiếng 'ực' trầm, ướt."""
    m = int(SR * 0.32)
    t = np.arange(m) / SR
    f = 240 * np.exp(-t * 9) + 70
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(m, 0.004, 0.07)
    click = hp(np.random.randn(m), 2500) * env(m, 0.0005, 0.006) * 0.6
    wet = lp(np.random.randn(m), 700) * env(m, 0.01, 0.05) * 0.5
    return tone + click + wet


def boing():
    """Tiếng "phụt" lò xo khi bị nhấc khỏi ghế."""
    m = int(SR * 0.45)
    t = np.arange(m) / SR
    f = 180 + 520 * (1 - np.exp(-t * 9)) + 40 * np.sin(2 * np.pi * 16 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(m, 0.003, 0.15) * 0.6


def bich():
    """Tiếng "bịch" rơi xuống đệm ghế."""
    m = int(SR * 0.3)
    return kick(0.3) * 0.9 + lp(np.random.randn(m), 300) * env(m, 0.001, 0.05) * 0.6


def xoet():
    """Tiếng bút lông gạch "xoẹt" trên giấy."""
    m = int(SR * 0.35)
    t = np.arange(m) / SR
    x = hp(np.random.randn(m), 2500) * np.sin(np.pi * t / t[-1]) ** 0.6
    return lp(x, 9000) * 0.5


def main():
    np.random.seed(11)
    n = int(SR * DAI)
    bed = np.zeros(n + SR)

    def put(x, t, g=1.0):
        i = int(t * SR)
        bed[i:i + len(x)] += x[: len(bed) - i] * g

    # 1. nhạc nhẹ, vui: lọc bớt sáng ở ngoài cửa, rõ dần khi vào máy, nhỏ lại khi anh nói, lên lại ở cuối
    m = nhac(DAI + 0.5, 100)[:n]
    tt = np.arange(n) / SR
    cut = int(SR * VAO_MAY)
    m[:cut] = lp(m[:cut], 1600) * 1.3
    g = np.interp(tt, [0, VAO_MAY - .1, VAO_MAY, NHO_LAI - .3, NHO_LAI, LEN_LAI - .2, LEN_LAI, DAI],
                  [0.45, 0.45, 0.55, 0.55, 0.22, 0.22, 0.75, 0.75])
    put(m * g, 0)

    # 2. SFX
    s = sfx()
    for t in (5.3, 10.2, 15.0, 29.2):             # chuyển cảnh (bỏ 22.4 vì che chữ "Hạ")
        put(s["whoosh"], t - 0.15, 0.3)
    for t in (2.3, 5.35, 10.6, 15.1, 17.95, 22.35):  # bong bóng
        put(s["pop"], t, 0.22)
    for t in (7.85, 8.15, 8.45):                 # "ực ực" khi tu nước, ngay sau câu nói
        put(uc(), t, 0.8)
    put(boing(), 10.3, 0.5)                      # bị nhấc khỏi ghế
    put(bich(), 14.05, 0.8)                      # rơi xuống ghế
    put(s["boom"], LEN_LAI, 0.35)
    put(s["ding"], 26.7, 0.28)                   # "Không biết chỉnh máy thì cứ hỏi..."
    put(xoet(), 29.35, 0.7)                      # gạch ô số 1
    put(s["ding"], 29.75, 0.3)

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
