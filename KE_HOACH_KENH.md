# Kế hoạch kênh TikTok: Gym và tâm lý người mới

> Ngách: **tâm lý người mới tập gym**, gồm sự ngại ngùng, sợ bị đánh giá, không biết bắt đầu từ đâu và hay bỏ cuộc.
> Lời hứa của kênh: *"Xem xong bạn bớt sợ và dám bước vào phòng gym."*
> Công cụ dựng: **Claude Code + HyperFrames** (viết video bằng HTML, render ra MP4 dọc 1080×1920).

---

## 1. HyperFrames có phù hợp không? **Có, rất phù hợp, với 2 lưu ý**

Tôi đã **cài và render thử** ngay trong môi trường này. HyperFrames bản `0.8.145`, Node 22, FFmpeg. File demo ở `videos/_starter/preview.mp4`.

| Tiêu chí | Kết quả |
|---|---|
| Video dọc TikTok 1080×1920 | ✅ Có sẵn (`hyperframes init --resolution portrait`) |
| Chữ tiếng Việt có dấu | ✅ Hiển thị chuẩn với font **Be Vietnam Pro** (đã nhúng sẵn trong starter) |
| Tốc độ render | ✅ Clip 6 giây render mất khoảng 10 giây, clip 45 giây ước tính 1 đến 2 phút |
| Chữ động, số đếm, hiệu ứng (GSAP) | ✅ Đây là thế mạnh chính |
| Phụ đề chạy theo giọng nói (karaoke caption) | ✅ Có Whisper, hỗ trợ tiếng Việt khi dùng model đa ngôn ngữ (`small`/`medium`, **không** dùng bản `.en`) |
| Ghép video quay thật (B-roll ở phòng gym) | ✅ Có, dùng `<video class="clip">` hoặc các skill `/talking-head-recut`, `/embedded-captions` |
| **Giọng đọc AI tiếng Việt** | ⚠️ **Không có sẵn.** TTS tích hợp (Kokoro) chỉ có các giọng Anh, Tây Ban Nha, Pháp, Hindi, Ý, Bồ Đào Nha, Nhật, Trung |
| Miễn phí, dùng thương mại | ✅ Giấy phép Apache 2.0, không tính phí theo lượt render |

**Lưu ý 1: Giọng đọc tiếng Việt.** Chọn một trong các cách sau:
1. **Tự thu giọng mình** (khuyến nghị). Kênh về tâm lý cần sự chân thật, giọng thật tạo niềm tin tốt hơn hẳn giọng AI. Chỉ cần thu bằng điện thoại trong phòng kín.
2. **Edge TTS** (miễn phí): giọng `vi-VN-HoaiMyNeural` (nữ) và `vi-VN-NamMinhNeural` (nam). Claude Code tạo được file mp3 bằng gói `edge-tts`.
3. **ElevenLabs** (trả phí) hoặc TTS của FPT.AI, Zalo AI, Viettel AI: giọng tự nhiên hơn.

Sau đó đưa file giọng vào: `npx hyperframes init ten-video --audio giong.mp3 --language vi --model small --resolution portrait`. HyperFrames sẽ tự nhận diện lời thoại để tạo phụ đề khớp từng chữ.

**Lưu ý 2: Mạng của môi trường.** Một số môi trường chặn CDN, nên starter đã **chép sẵn GSAP và font vào thư mục dự án**, không tải từ mạng. Cách này cũng làm render ổn định hơn.

**Khi nào HyperFrames *không* đủ?** Khi bạn cần cảnh người thật tập luyện. HyperFrames không tự quay hay tạo cảnh người. Cách làm tốt nhất là **kết hợp**: quay vài cảnh B-roll thật ở phòng gym (đôi giày, cửa phòng tập, tạ, dáng người từ phía sau), rồi để HyperFrames phủ chữ động và phụ đề lên trên.

---

## 2. Vì sao ngách này có đất?

- Từ khoá **"gymtimidation"** (gym + intimidation, nghĩa là sợ phòng gym) là hiện tượng có thật và được báo chí sức khoẻ viết nhiều.
- Trend **#shygirlworkout** (bài tập cho người ngại, tập ở góc yên tĩnh) từng đạt **hơn 500 triệu lượt xem** trên TikTok. Bình luận điển hình: *"Mình muốn tập lắm nhưng sợ bị người ta đánh giá."*
- Khảo sát (do doanh nghiệp tài trợ, chỉ nên tham khảo): khoảng **51% người tập gym ở Mỹ** từng thấy bị nhìn ngó hoặc đánh giá. Theo ASICS, **68%** người lớn ngại đến gym vì thấy mình "không giống dân tập gym". Một nghiên cứu khoa học (n=384) cho thấy khoảng **36%** có mức lo âu cao liên quan đến phòng gym.
- **Hiệu ứng ánh đèn sân khấu** (spotlight effect, Gilovich và cộng sự, 2000): người mặc áo "gây xấu hổ" đoán khoảng **50%** người xung quanh để ý tới mình, thực tế chỉ khoảng **25%**. Đây là "vũ khí" khoa học rất mạnh cho kênh.
- Ở thị trường Việt Nam, đa số kênh gym tập trung vào kỹ thuật và giáo án. **Mảng tâm lý người mới còn ít người làm tử tế**, nên đây là lợi thế để bạn khác biệt.

> ⚠️ Các số liệu khảo sát chỉ nên dùng kèm chữ "khoảng" hoặc "một khảo sát cho thấy", không nói như sự thật tuyệt đối. Nên ghi nguồn trong phần mô tả hoặc bình luận ghim.

---

## 3. Bốn trụ nội dung (content pillars)

| Trụ | Mục đích | Tỉ lệ |
|---|---|---|
| **A. Gỡ nỗi sợ** | Tâm lý, khoa học hành vi, "bạn không cô đơn" | 40% |
| **B. Hướng dẫn sinh tồn ngày đầu** | Thực hành: làm gì, mặc gì, dùng máy ra sao, quy tắc ngầm | 30% |
| **C. Kể chuyện / POV** | Đồng cảm, hài nhẹ, giúp video dễ lan truyền | 20% |
| **D. Cộng đồng** | Trả lời bình luận, thử thách 30 ngày, kể câu chuyện người xem | 10% |

---

## 4. Ngân hàng 20 ý tưởng video (kèm câu mở đầu)

Câu mở đầu phải nằm trong **1 đến 2 giây đầu**, vừa hiện chữ to trên màn hình vừa được đọc thành tiếng.

### A. Gỡ nỗi sợ
1. **"Bạn nghĩ cả phòng gym đang nhìn bạn? Khoa học nói chỉ khoảng một nửa số đó."** Giải thích hiệu ứng ánh đèn sân khấu, minh hoạ bằng số đếm 50% → 25%.
2. **"Người cơ bắp nhất phòng gym đang nghĩ gì khi thấy bạn?"** Họ đang đếm rep, nghe nhạc, soi form của chính mình. Không ai rảnh để đánh giá bạn.
3. **"Ai cũng từng là người mới, kể cả ông to nhất phòng."** Dựng hình ảnh ngày đầu và hiện tại theo kiểu so sánh.
4. **"3 suy nghĩ khiến bạn mãi không dám đi tập."** "Mình béo quá", "mình không biết dùng máy", "người ta cười mình". Bẻ từng suy nghĩ một.
5. **"Cảm giác ngại ở phòng gym là bình thường. Đây là lý do não bạn làm vậy."** Não coi môi trường lạ là mối đe doạ. Cảm giác này giảm dần sau khoảng 3 đến 5 buổi khi đã quen.
6. **"Đừng đợi hết sợ mới đi tập."** Hành động trước, tự tin đến sau.

### B. Hướng dẫn sinh tồn
7. **"Checklist ngày đầu đi gym: lưu lại để khỏi bối rối."** Dạng danh sách, mỗi mục hiện ra kèm dấu ✓. Kiểu video này được lưu nhiều.
8. **"Giáo án 30 phút cho người ngại: chỉ dùng 1 góc, không cần chen máy."** Phiên bản Việt của #shygirlworkout.
9. **"5 quy tắc ngầm ở phòng gym không ai nói cho bạn."** Lau máy, cất tạ, hỏi "anh còn mấy hiệp?", không đứng chắn gương.
10. **"Câu nói giúp bạn xin dùng chung máy mà không ngại."** Kịch bản giao tiếp mẫu.
11. **"Nên đi gym giờ nào để vắng người?"** Gợi ý khung giờ vắng như sáng sớm, đầu giờ chiều.
12. **"Mặc gì đi gym lần đầu để không thấy lạc lõng?"**
13. **"Không biết tập gì? Hãy nhờ PT hoặc lễ tân hướng dẫn, đó là việc của họ."** Đa số phòng gym có buổi hướng dẫn miễn phí.

### C. Kể chuyện / POV
14. **"POV: Ngày đầu bạn bước vào phòng gym."** Dạng hội thoại nội tâm, chữ hiện ra như suy nghĩ. Hài nhẹ và dễ đồng cảm.
15. **"Những thứ người mới sợ, so với thực tế."** Màn hình chia đôi kiểu meme "Kỳ vọng / Thực tế".
16. **"Tin nhắn gửi bạn của 3 tháng sau."** Giọng ấm, nhạc piano, đánh vào cảm xúc.
17. **"Mình từng đứng ngoài cửa phòng gym 15 phút rồi đi về."** Chuyện thật của bạn. Người xem đồng cảm rất mạnh với loại này.

### D. Cộng đồng
18. **"Trả lời bình luận: 'Mình béo, đi gym có bị cười không?'"** Dùng tính năng trả lời bình luận bằng video của TikTok.
19. **"Thử thách 30 ngày: chỉ cần ĐẾN phòng gym, tập bao nhiêu cũng được."** Làm thành chuỗi nhiều tập.
20. **"Câu chuyện người xem: lần đầu đi gym của bạn thế nào?"** Biến bình luận thành nội dung.

---

## 5. Kịch bản chi tiết video #1

**Tiêu đề:** *"Bạn ngại lần đầu đến phòng gym? Xem cái này trước."*
**Độ dài:** khoảng 40 giây. **Phong cách:** nền tối, chữ trắng, điểm nhấn xanh chanh `#c6ff3d`, xen B-roll phòng gym nếu có.

| Thời gian | Hình ảnh (HyperFrames) | Lời đọc |
|---|---|---|
| 0–2s | Chữ to bật vào: **"Bạn nghĩ CẢ PHÒNG GYM đang nhìn bạn?"** + hiệu ứng rung nhẹ | "Bạn nghĩ cả phòng gym đang nhìn bạn?" |
| 2–7s | Biểu tượng con mắt nhân bản ra khắp màn hình, sau đó vỡ tan | "Lần đầu đi tập, ai cũng có cảm giác đó: sợ làm sai, sợ bị cười, sợ trông lạc lõng." |
| 7–16s | Thẻ "Nghiên cứu Đại học Cornell, 2000". Số đếm **50%** (người ta *nghĩ*) chuyển thành **25%** (thực tế) | "Các nhà tâm lý học gọi đó là hiệu ứng ánh đèn sân khấu. Người ta đoán có một nửa số người xung quanh để ý mình, thực tế chỉ khoảng một phần tư." |
| 16–24s | Ba thẻ lần lượt trượt vào: 🎧 "Đang nghe nhạc", 🔢 "Đang đếm rep", 🪞 "Đang soi form mình" | "Ở phòng gym còn ít hơn nữa. Ai cũng đang bận với hiệp tập của chính họ." |
| 24–34s | Checklist 3 mục hiện dấu ✓: "Đi giờ vắng", "Có sẵn 3 bài tập", "Đeo tai nghe" | "Mẹo cho buổi đầu: đi giờ vắng, chuẩn bị sẵn 3 bài tập, đeo tai nghe vào. Thế là đủ." |
| 34–40s | Chữ: **"Người mạnh nhất phòng cũng từng có buổi đầu tiên."** + nút "Theo dõi để đi cùng mình" | "Người mạnh nhất phòng cũng từng có buổi đầu tiên. Theo dõi để mình đồng hành cùng bạn nhé." |

**Phụ đề:** chạy karaoke theo từng chữ, đặt ở vùng giữa dưới, cách đáy khoảng 400px để không bị nút TikTok che.
**Chú thích (caption):** "Lần đầu đi gym bạn sợ điều gì nhất? 👇 #gym #nguoimoitapgym #tamly #gymtimidation #tapgym"
**Câu hỏi cuối video:** kêu gọi bình luận để lấy ý tưởng cho các video trả lời bình luận sau.

> Cảnh 0 đến 16 giây đã có bản nháp trong `videos/_starter/index.html`. Đó chính là bản render thử.

---

## 6. Quy trình sản xuất mỗi video với Claude Code

```
1. Chọn ý tưởng → nhờ Claude viết kịch bản (bảng thời gian | hình | lời)
2. Thu giọng (tự thu, Edge TTS hoặc ElevenLabs) → giong.mp3
3. Copy videos/_starter → videos/<so>-<ten-video>/
4. Gọi Claude: "Dùng /hyperframes, dựng video theo kịch bản X với giong.mp3,
   phong cách giống _starter, có phụ đề karaoke tiếng Việt"
5. npm run dev   → xem trước trên trình duyệt, nhờ Claude chỉnh
6. npm run check → kiểm tra lỗi
7. npm run render → ra MP4 1080×1920, đăng TikTok
```

**Cài skill HyperFrames cho Claude Code trên máy bạn** (để Claude dựng đúng chuẩn framework):
```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
# yêu cầu: Node.js 22+, FFmpeg
```

Các skill nên dùng: `/faceless-explainer` (video giải thích không lộ mặt), `/motion-graphics` (chữ động, số đếm), `/embedded-captions` và `/talking-head-recut` (khi bạn quay mặt hoặc quay B-roll thật).

---

## 7. Nhận diện và nguyên tắc chung

- **Màu:** nền đen `#0b0b0f`, chữ trắng, một màu nhấn duy nhất là xanh chanh `#c6ff3d`. Giữ cố định để người xem nhận ra kênh.
- **Font:** Be Vietnam Pro, đậm 900 cho câu mở đầu, 600 cho nội dung.
- **Nhịp:** cứ 2 đến 3 giây đổi hình hoặc hiện chữ mới. Độ dài 30 đến 60 giây.
- **Vùng an toàn:** tránh 250px dưới cùng và cột 150px bên phải, vì nút của TikTok nằm ở đó.
- **Giọng điệu:** như người anh hoặc chị đi trước, ấm áp, không phán xét, **không chê cơ thể**.
- **Tần suất:** 3 đến 5 video mỗi tuần. Tuần đầu đăng ý tưởng #1, #7, #14 để thử phản ứng của 3 trụ nội dung.
- **Ghi nhãn AI:** nếu dùng giọng AI, bật nhãn "nội dung do AI tạo" của TikTok để tránh bị giảm phân phối.
- **Không đưa lời khuyên y tế.** Với các chủ đề lo âu nặng, nên nói thêm "nếu bạn thấy quá sức, hãy tìm chuyên gia".

---

## Nguồn tham khảo

- HyperFrames (GitHub): https://github.com/heygen-com/hyperframes
- HyperFrames trên Claude: https://claude.com/connectors/hyperframes-heygen
- Hướng dẫn HyperFrames + Claude Code: https://themenonlab.blog/blog/hyperframes-claude-code-writes-renders-videos
- Trend #shygirlworkout (Healthline): https://www.healthline.com/health-news/shy-girl-workout-how-this-tiktok-trend-can-help-ease-gym-anxiety
- Gymtimidation (CNN qua KTVZ): https://ktvz.com/health/cnn-health/2023/08/27/do-you-have-gymtimidation-heres-how-to-fix-it/
- Khảo sát gymtimidation (Musclebooster): https://musclebooster.welltech.com/gymtimidation-us
- Khảo sát ASICS 68%: https://news.yahoo.com/how-to-overcome-gym-embarrassment-070048026.html
- Nghiên cứu lo âu phòng gym (IJCMPH): https://www.ijcmph.com/index.php/ijcmph/article/download/15661/9523/82527
- Mẹo vượt nỗi sợ phòng gym (Experience Life): https://experiencelife.lifetime.life/article/8-tips-to-overcome-fear-of-going-to-the-gym/
- Hiệu ứng ánh đèn sân khấu: https://www.reachlink.com/advice/general/nobody-is-watching-you-nearly-as-closely-as-you-think/
