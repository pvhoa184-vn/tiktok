"""Tạo các câu giọng AI cho video Ngày 1/100 (VieNeu-TTS v3 Turbo).

Bé Đậu: nhân bản từ giọng EverAI của người dùng. Anh tập lâu: giọng có sẵn.
Chạy:  python tao_giong_ngay1.py <file giọng mẫu .wav 3-15 giây>
Đầu ra: giong/*.raw.wav (chưa xử lý). am_thanh.py lo phần thì thầm và trộn.
"""
import sys
from pathlib import Path

from vieneu import Vieneu

REF = sys.argv[1]
CO_BAP = "Quốc Tuấn"
CAU = {
    "1-dem": ("ref", "Rồi. Đếm tới ba là vào. Một. Hai..."),
    "2-khoan": ("ref", "Khoan. Uống miếng nước, cái đã."),  # dấu phẩy để đọc rõ "cái đã"
    "3-bay-len": ("ref", "Ủa. Kéo xuống mà mình bay lên."),
    "4-hoi-thu": ("ref", "Chắc ảnh đợi máy. Thôi, hỏi thử."),
    "5-anh-oi": ("ref", "Anh ơi, máy này chỉnh sao vậy anh? Em tập nhanh rồi nhường anh."),
    "co-bap": ("voice", "Hạ cái đệm này xuống nè. Anh không đợi máy đâu, em cứ tập."),
}
tts = Vieneu(mode="v3turbo")
Path("giong").mkdir(exist_ok=True)
for ten, (kieu, cau) in CAU.items():
    wav = tts.infer(cau, ref_audio=REF) if kieu == "ref" else tts.infer(cau, voice=CO_BAP)
    tts.save(wav, f"giong/{ten}.raw.wav")
    print("xong", ten)
