# Kênh TikTok: Tâm lý người mới tập gym

Trả lời người dùng bằng **tiếng Việt**. Kế hoạch đầy đủ nằm trong `KE_HOACH_KENH.md`, nên đọc file đó khi cần chi tiết.

## Các quyết định đã chốt
- **Định vị:** "Đồng hành tâm lý 90 ngày đầu tập gym: từ sợ bước vào đến không muốn bỏ." Thị trường **Việt Nam** trước, có thể làm kênh tiếng Anh sau.
- **Công cụ dựng:** HyperFrames (HTML → MP4), khổ dọc 1080×1920, 30fps. Mẫu dựng sẵn ở `videos/_starter/` đã có GSAP và font Be Vietnam Pro chép sẵn trong thư mục. **Không tải từ CDN**, vì môi trường cloud chặn jsdelivr và Hugging Face.
- **Giọng đọc:** VieNeu-TTS (`pip install vieneu`, bản v3 Turbo, mã nguồn Apache 2.0), nhân bản giọng người dùng từ 3–8 giây thu âm. TTS tích hợp của HyperFrames (Kokoro) không có tiếng Việt.
- **Phụ đề:** dùng `hyperframes init <ten> --audio giong.mp3 --language vi --model small --resolution portrait` (Whisper đa ngôn ngữ, không dùng bản `.en`).
- **Hình ảnh mỗi cảnh có 3 lớp:** nền là B-roll phòng gym (tự quay hoặc lấy từ Pexels/Pixabay), minh hoạ là **nhân vật đại diện "người mới"** vẽ bằng SVG cùng icon động, trên cùng là chữ và phụ đề karaoke.
- **Nhận diện:** nền `#0b0b0f`, chữ trắng, một màu nhấn xanh chanh `#c6ff3d`. Tránh 250px dưới cùng và cột 150px bên phải (nút của TikTok).
- **Số liệu:** chỉ nói "khoảng", nói rõ nguồn, không đưa lời khuyên y tế. Bật nhãn AI trên TikTok khi dùng giọng AI.

## Cấu trúc thư mục
- `KE_HOACH_KENH.md`: kế hoạch, bản đồ chủ đề, kịch bản video #1
- `videos/_starter/`: mẫu HyperFrames; sao chép thành `videos/<so>-<ten>/` cho mỗi video
- `assets/voice/`: file giọng mẫu của người dùng (khi có)
- `assets/nhan-vat/`: SVG nhân vật đại diện
- `scripts/tao_giong.py`: tạo giọng đọc bằng VieNeu-TTS

## Tiến độ (cập nhật cuối mỗi session)
- [x] Nghiên cứu ngách, đánh giá HyperFrames, render thử
- [x] Bản đồ chủ đề 90 ngày, chọn thị trường Việt, chọn VieNeu-TTS
- [ ] Người dùng gửi file thu âm giọng mẫu (câu mẫu: "Chào bạn, mình từng rất ngại khi lần đầu bước vào phòng gym. Nếu bạn cũng đang sợ bị người khác nhìn, đừng lo nhé, ai cũng từng bắt đầu như vậy. Hôm nay mình sẽ chỉ bạn vài mẹo nhỏ để tự tin hơn.")
- [x] Script tạo giọng `scripts/tao_giong.py` (VieNeu 3.8.3, API: `Vieneu(mode="v3turbo").infer(text, ref_audio=...)`, 48kHz, có watermark âm thanh mặc định). **Môi trường cloud không chạy được** vì mô hình chỉ tải từ Hugging Face (bị chặn), nên phải chạy trên máy local.
- [x] Lời đọc video #1: `videos/01-ngai-lan-dau/loi_doc.txt`
- [x] Vẽ 3 phương án nhân vật (SVG, mỗi nhân vật có bản "ngại" và "tự tin") trong `assets/nhan-vat/`, bảng so sánh `bang-so-sanh.png`: A. Bé Đậu, B. Cậu Hoodie, C. Tạ Tí
- [ ] Người dùng chọn nhân vật
- [ ] Chạy `python scripts/tao_giong.py --ref assets/voice/mau.m4a --file videos/01-ngai-lan-dau/loi_doc.txt --out videos/01-ngai-lan-dau/giong.wav` trên máy local
- [ ] Dựng video #1 (kịch bản ở mục 6 của `KE_HOACH_KENH.md`)
- [ ] Chưa chốt: cảnh nền tự quay hay lấy từ Pexels
