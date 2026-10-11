# Video #1: Ngày 1/90

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
- Giọng thì thầm: thu 4 câu, lưu vào `giong/` đúng tên trong `GIONG` của `am_thanh.py`, chạy lại `python3 am_thanh.py`. Thiếu file nào thì câu đó chỉ có chữ.
