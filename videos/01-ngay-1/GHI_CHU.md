# Video #1: Ngày 1/90 (bản 2)

Bản 2 (11/10): anh cơ bắp tới chỉnh tạ giúp thay cho đoạn "nhăn mặt tưởng cười", bỏ trích nghiên cứu, thêm giọng AI.

Kịch bản: `/mnt/project-files/kich-ban/01-ngay-1/kich-ban.md` (chữ trên màn hình lấy nguyên văn từ `loi-va-chu.txt`, đã qua `soat_kich_ban.py`).

## Dựng lại
```
npx --yes hyperframes@0.8.145 render -o renders/hinh.mp4   # hình
python3 am_thanh.py                                         # nhạc + SFX + giọng (nếu có) → renders/final.mp4
```

## Hình
- `assets/canh/*.jpg`: cảnh phòng gym 9:16, tạo bằng `nano-banana-pro` trên kie.ai, ảnh tham chiếu là ảnh gốc trong `assets/nhan-vat/goc/ngay-1/`.
- `assets/clip/*.mp4`: Kling 3.0 omni image-to-video 1080p, 5 giây (cửa: từ `be-dau-nep-cua-9x16.png`; tai nghe, squat: từ ảnh trong `assets/canh/`). Đã chuyển sang 30fps, keyframe mỗi giây.

## Âm thanh
- Nhạc và SFX tự tổng hợp trong `am_thanh.py` (không bản quyền): nhạc hồi hộp tới 13,4 giây, rít đĩa, im lặng, nhạc vui vào nhẹ ở 16,4 giây, lên hẳn ở 19,2 giây, tiếng "ực" ở 25 giây.
- Muốn dùng nhạc trend: đăng video lên TikTok, chọn nhạc trong app, chỉnh âm lượng gốc xuống.
- Giọng AI (VieNeu v3 Turbo): `python tao_giong_ngay1.py <giọng mẫu 12 giây>` (venv có `vieneu` và `onnxruntime<1.24`). Bé Đậu nhân bản từ `assets/voice/mau-nghe-thu/everai - giong ban nhan ban.mp3` (cắt 12 giây đầu), anh cơ bắp là giọng có sẵn "Quốc Tuấn". File `.wav` bị gitignore, chạy lại script để tạo.
- Thu giọng thật: ghi đè file trong `giong/` đúng tên trong `GIONG` của `am_thanh.py`, chạy lại `python3 am_thanh.py`.
- Kiểm tra: Whisper medium trên đoạn 2,4–16,4 giây của bản trộn nghe đúng lời. Chạy trên cả video thì Whisper hay bịa lời ở đoạn chỉ có nhạc, nên cắt đoạn có giọng ra mà soát.
