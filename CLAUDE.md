# Kênh TikTok: Tâm lý người mới tập gym

Trả lời người dùng bằng **tiếng Việt**. Kế hoạch đầy đủ nằm trong `KE_HOACH_KENH.md`, nên đọc file đó khi cần chi tiết.

## Các quyết định đã chốt
- **Định vị:** "Đồng hành tâm lý 90 ngày đầu tập gym: từ sợ bước vào đến không muốn bỏ." Thị trường **Việt Nam** trước, có thể làm kênh tiếng Anh sau.
- **Công cụ dựng:** HyperFrames (HTML → MP4), khổ dọc 1080×1920, 30fps. Mẫu dựng sẵn ở `videos/_starter/` đã có GSAP và font Be Vietnam Pro chép sẵn trong thư mục. **Không tải từ CDN**, vì môi trường cloud chặn jsdelivr và Hugging Face. Mạng đã mở thêm `pexels.com`, `*.pexels.com`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`. Lệnh `npx hyperframes` cần tải mạng (transcribe…) phải chạy với `NODE_USE_ENV_PROXY=1`.
- **Giọng đọc:** VieNeu-TTS (`pip install vieneu`, bản v3 Turbo, mã nguồn Apache 2.0), **ưu tiên giọng có sẵn** (25 giọng, `--voice "Tên"`, xem `--list-voices`) làm "giọng của Bé Đậu"; nhân bản giọng người dùng (`--ref`) là phương án phụ. Mẫu nghe thử trong `assets/voice/mau-nghe-thu/`. TTS tích hợp của HyperFrames (Kokoro) không có tiếng Việt.
- **Phụ đề:** dùng `hyperframes init <ten> --audio giong.mp3 --language vi --model small --resolution portrait` (Whisper đa ngôn ngữ, không dùng bản `.en`).
- **Hình ảnh mỗi cảnh có 3 lớp:** nền là B-roll Pexels trong `assets/broll/` (thẻ `<video class="clip" muted>` ở track 0, CSS `filter:blur(7px) brightness(.32)`), minh hoạ là **nhân vật Bé Đậu** (PNG 3D) cùng icon 3D Fluent Emoji, trên cùng là chữ và phụ đề karaoke.
- **Nhận diện:** nền `#0b0b0f`, chữ trắng, một màu nhấn xanh chanh `#c6ff3d`. Tránh 250px dưới cùng và cột 150px bên phải (nút của TikTok).
- **Số liệu:** chỉ nói "khoảng", nói rõ nguồn, không đưa lời khuyên y tế. Bật nhãn AI trên TikTok khi dùng giọng AI.

## Cấu trúc thư mục
- `KE_HOACH_KENH.md`: kế hoạch, bản đồ chủ đề, kịch bản video #1
- `videos/_starter/`: mẫu HyperFrames; sao chép thành `videos/<so>-<ten>/` cho mỗi video
- `assets/voice/`: file giọng mẫu của người dùng (khi có)
- `assets/nhan-vat/`: Bé Đậu PNG nền trong suốt (`be-dau-ngai`, `be-dau-nup-cua`, `be-dau-tai-nghe`, `be-dau-nang-ta`, `be-dau-tu-tin`, `be-dau-chao`); ảnh gốc ChatGPT ở `goc/`; `nhap-svg/` là bản nháp cũ, không dùng
- `assets/broll/`: video nền Pexels đã chuẩn hoá 1080×1920, 30fps, keyframe mỗi giây; xem `NGUON.md` để biết nội dung và link gốc
- `assets/icons-3d/`: icon Fluent Emoji 3D (MIT)
- `scripts/tach_nen.py`: cắt bảng nhân vật và tách nền trắng thành PNG trong suốt
- `scripts/tao_giong.py`: tạo giọng đọc bằng VieNeu-TTS

## Tiến độ (cập nhật cuối mỗi session)
- [x] Nghiên cứu ngách, đánh giá HyperFrames, render thử
- [x] Bản đồ chủ đề 90 ngày, chọn thị trường Việt, chọn VieNeu-TTS
- [ ] Người dùng gửi file thu âm giọng mẫu (câu mẫu: "Chào bạn, mình từng rất ngại khi lần đầu bước vào phòng gym. Nếu bạn cũng đang sợ bị người khác nhìn, đừng lo nhé, ai cũng từng bắt đầu như vậy. Hôm nay mình sẽ chỉ bạn vài mẹo nhỏ để tự tin hơn.")
- [x] Script tạo giọng `scripts/tao_giong.py` (VieNeu 3.8.3, API: `Vieneu(mode="v3turbo").infer(text, ref_audio=...)`, 48kHz, có watermark âm thanh mặc định). Chạy được trên cloud (khoảng 20 giây mỗi đoạn ngắn, chạy bằng CPU), với điều kiện **cài `onnxruntime<1.24`** (bản 1.29 báo lỗi "External data path escapes model directory" do cache Hugging Face dùng symlink). Môi trường Python: tạo venv rồi `pip install vieneu "onnxruntime<1.24"`.
- [x] Lời đọc video #1: `videos/01-ngai-lan-dau/loi_doc.txt`
- [x] Vẽ 3 phương án nhân vật (SVG, mỗi nhân vật có bản "ngại" và "tự tin") trong `assets/nhan-vat/`, bảng so sánh `bang-so-sanh.png`: A. Bé Đậu, B. Cậu Hoodie, C. Tạ Tí
- [x] Người dùng chê nét vẽ SVG tay là xấu. Đã chuyển sang **icon 3D Fluent Emoji của Microsoft** (MIT) trong `assets/icons-3d/`, tải từ `raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/<Tên>/3D/<ten>_3d.png` (đi được qua proxy). 
- [x] **Chốt nhân vật Bé Đậu**: người dùng tạo bằng ChatGPT (hạt đậu kem 3D, băng đô xanh chanh), đã tách thành 6 PNG trong suốt.  Cần tư thế mới thì người dùng tạo thêm trên ChatGPT với ảnh gốc làm tham chiếu ("same character, ..., plain white background"), rồi chạy `tach_nen.py`.
- [x] Đã thử 2 giọng nam "Thiện Minh" và "Hải Đăng" (`assets/voice/mau-nghe-thu/v3 - *.mp3`), Whisper `small --language vi` nhận đúng lời (chỉ nghe nhầm "gym" thành "Jim", cần sửa tay trong phụ đề). Lý do chọn giọng nam: khán giả gym Việt có vẻ nghiêng về nam, và nỗi sợ của nam ít được nói tới.
- [ ] Người dùng chọn giọng có sẵn, rồi chạy `python scripts/tao_giong.py --voice "<Tên>" --file videos/01-ngai-lan-dau/loi_doc.txt --out videos/01-ngai-lan-dau/giong.wav` trên máy local
- [ ] Dựng video #1 (kịch bản ở mục 6 của `KE_HOACH_KENH.md`)
- [x] Cảnh nền: lấy từ Pexels. Tải không cần API key qua `https://www.pexels.com/download/video/<ID>/` (chuyển hướng sang videos.pexels.com); tìm ID bằng WebSearch giới hạn ở pexels.com. Trang tìm kiếm Pexels bị Cloudflare chặn (403). Video phải mã hoá lại với `-g 30 -keyint_min 30`, nếu không HyperFrames báo lỗi keyframe thưa và hình bị đứng. Demo đủ 3 lớp: `videos/01-ngai-lan-dau/demo-co-nen.mp4`
