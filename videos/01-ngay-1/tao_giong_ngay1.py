"""Tạo các câu giọng AI cho video Ngày 1/90 (VieNeu-TTS v3 Turbo).

Bé Đậu: nhân bản từ giọng EverAI của người dùng. Anh cơ bắp: giọng có sẵn.
Chạy:  python tao_giong_ngay1.py <file giọng mẫu .wav 3-15 giây>
Đầu ra: giong/*.raw.wav (chưa xử lý). am_thanh.py lo phần thì thầm và trộn.
"""
import sys
from pathlib import Path

from vieneu import Vieneu

REF = sys.argv[1]
CO_BAP = "Quốc Tuấn"
CAU = {
    "1-muoi-phut": ("ref", "Mười phút rồi. Vẫn chưa dám vào."),
    "2-gia-vo": ("ref", "Giả vờ nghe điện thoại. Không ai gọi cả."),
    "3-cam-vay": ("ref", "Cầm vậy là đúng chưa ta?"),
    "4-thoi-xong": ("ref", "Thôi xong. Ảnh đi về phía mình."),
    "co-bap": ("voice", "Cầm thế này nè. Hồi đầu anh cũng cầm ngược."),
}
tts = Vieneu(mode="v3turbo")
Path("giong").mkdir(exist_ok=True)
for ten, (kieu, cau) in CAU.items():
    wav = tts.infer(cau, ref_audio=REF) if kieu == "ref" else tts.infer(cau, voice=CO_BAP)
    tts.save(wav, f"giong/{ten}.raw.wav")
    print("xong", ten)
