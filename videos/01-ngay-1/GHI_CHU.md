# Video #1: Ngày 1/100 (bản 3)

Bản 3 (12/10): máy kéo xô quên hạ đệm giữ đùi, Bé Đậu tự hỏi anh tập lâu. Series đổi tên "100 ngày thay đổi bản thân của Bé Đậu".

Kịch bản: `/mnt/project-files/kich-ban/01-ngay-1/kich-ban.md` (chữ trên màn hình lấy nguyên văn từ `loi-va-chu.txt`, đã qua `soat_kich_ban.py`). Bản 2 (Ngày 1/90) đã thay, file cũ `assets/canh/`, `assets/clip/`, `ngay-1-90.mp4` giữ lại để tham khảo.

## Dựng lại
```
npx --yes hyperframes@0.8.145 render -o renders/hinh.mp4   # hình, 32,4 giây
python3 am_thanh.py                                         # nhạc + SFX + giọng → renders/final.mp4
```

## Hình
- `assets/canh-v3/*.jpg`: người dùng tạo trên ChatGPT theo `prompt-anh-v3.md` (ảnh gốc PNG ở `/mnt/project-files/kich-ban/01-ngay-1/anh/`). Riêng `canh-6-anh-dung-canh` tạo bằng `nano-banana-pro` trên kie.ai, tham chiếu `canh-7` và `canh-5`.
- `assets/clip-v3/*.mp4`: Kling 3.0 omni image-to-video 1080p, 5 giây, từ `canh-1`, `canh-5`, `canh-7`. Đã cắt bỏ đoạn Kling làm quá:
  - `bi-nhac`: lấy 0–3,2 giây (sau đó Bé Đậu ngã lăn xuống sàn, không thật), chậm 1,2 lần, giữ khung cuối 1 giây.
  - `chi-dem`: lấy 0–3,6 giây (sau đó anh đi xuyên qua sau lưng Bé Đậu), giữ khung cuối 0,5 giây.
  - Chuẩn hoá: 30fps, keyframe mỗi giây.
- Cảnh 8 đổi qua lại 2 ảnh (`8a` tay trên, `8b` kéo xuống) cho giống đang kéo.

## Âm thanh
- Nhạc và SFX tự tổng hợp trong `am_thanh.py` (không bản quyền): nhạc vui lọc bớt sáng ở ngoài cửa, rõ hơn từ 10,2 giây, nhỏ lại lúc anh tập lâu nói (22,4), lên lại ở 26,4. SFX: "ực ực", "phụt" khi bị nhấc, "bịch" khi rơi xuống ghế, "xoẹt" khi gạch lịch.
- Giọng AI (VieNeu v3 Turbo): `python tao_giong_ngay1.py <giọng mẫu 12 giây>` (venv có `vieneu` và `onnxruntime<1.24`). Bé Đậu nhân bản từ `assets/voice/mau-nghe-thu/everai - giong ban nhan ban.mp3` (cắt 12 giây đầu), anh tập lâu là giọng có sẵn "Quốc Tuấn". VieNeu mỗi lần đọc ra hơi khác: tạo vài bản, chọn bản Whisper nghe đúng chữ. File `.wav` bị gitignore.
- Thu giọng thật: ghi đè file trong `giong/` đúng tên trong `GIONG` của `am_thanh.py`, chạy lại `python3 am_thanh.py`.
- Kiểm tra: Whisper medium trên đoạn có giọng của bản trộn (chạy trên cả video thì Whisper hay bịa lời ở đoạn chỉ có nhạc). Nếu `whisper-cli` báo "Illegal instruction" (máy cloud đổi CPU), build lại: `cmake -B build -DGGML_NATIVE=OFF && cmake --build build -j4 --target whisper-cli` trong `~/.cache/hyperframes/whisper/whisper.cpp`.
