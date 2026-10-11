"""Tạo giọng đọc tiếng Việt bằng VieNeu-TTS, nhân bản từ giọng mẫu của bạn.

Cài đặt (một lần):  pip install vieneu
Cách dùng (giọng có sẵn):
    python scripts/tao_giong.py --voice "Trúc Ly" \
        --file videos/01-ngai-lan-dau/loi_doc.txt \
        --out videos/01-ngai-lan-dau/giong.wav
    python scripts/tao_giong.py --list-voices      # xem danh sách giọng có sẵn

Cách dùng (nhân bản giọng của bạn):
    python scripts/tao_giong.py --ref assets/voice/mau.m4a \
        --file videos/01-ngai-lan-dau/loi_doc.txt \
        --out videos/01-ngai-lan-dau/giong.wav

Mỗi dòng trống trong file lời đọc là một đoạn ngắt (dừng lâu hơn một chút).
Lần chạy đầu sẽ tải mô hình từ Hugging Face (vài trăm MB).
"""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Tạo giọng đọc bằng VieNeu-TTS")
    who = ap.add_mutually_exclusive_group()
    who.add_argument("--ref", help="File giọng mẫu để nhân bản (3–15 giây, m4a/mp3/wav)")
    who.add_argument("--voice", help='Tên giọng có sẵn của VieNeu, vd. "Trúc Ly"')
    ap.add_argument("--list-voices", action="store_true", help="In danh sách giọng có sẵn rồi thoát")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="Câu cần đọc")
    src.add_argument("--file", help="File .txt chứa lời đọc")
    ap.add_argument("--out", default="giong.wav", help="File đầu ra (.wav hoặc .mp3)")
    ap.add_argument("--mode", default="v3turbo", choices=["v3turbo", "v3nano"],
                    help="v3nano nhanh hơn trên máy yếu nhưng chất lượng kém hơn")
    args = ap.parse_args()

    if args.list_voices:
        import json
        import vieneu
        data = json.loads((Path(vieneu.__file__).parent / "assets" / "voices_v3_turbo.json").read_text(encoding="utf-8"))
        for name, v in data["presets"].items():
            print(f"{name:16} {v.get('description', '')}")
        return
    if not (args.text or args.file):
        ap.error("cần --text hoặc --file")
    if not (args.ref or args.voice):
        ap.error("cần --voice (giọng có sẵn) hoặc --ref (nhân bản giọng)")

    text = args.text if args.text else Path(args.file).read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("Lời đọc đang trống.")

    ref = Path(args.ref) if args.ref else None
    # VieNeu đọc wav ổn định nhất, nên đổi m4a/mp3 sang wav trước.
    if ref and ref.suffix.lower() != ".wav":
        wav_ref = ref.with_suffix(".ref.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(ref),
                        "-ac", "1", "-ar", "44100", str(wav_ref)], check=True)
        ref = wav_ref

    from vieneu import Vieneu

    tts = Vieneu(mode=args.mode)
    wav = tts.infer(text, ref_audio=str(ref)) if ref else tts.infer(text, voice=args.voice)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".mp3":
        tmp = out.with_suffix(".tmp.wav")
        tts.save(wav, str(tmp))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp),
                        "-b:a", "192k", str(out)], check=True)
        tmp.unlink()
    else:
        tts.save(wav, str(out))
    print(f"Đã tạo: {out}")


if __name__ == "__main__":
    main()
