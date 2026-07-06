## 1. Phân tích Tỷ lệ rác (Noise Analysis)
- Mean Noise (43%): Trung bình gần một nửa nội dung file của bạn là các thẻ HTML rác. Nếu đưa thẳng vào LangChain/LLM, bạn sẽ lãng phí 43% chi phí token và làm loãng ngữ cảnh.

- Max Noise (100%): Dữ liệu tồn tại các file "rỗng" (chỉ chứa khung HTML nhưng không có chữ, hoặc chỉ toàn khoảng trắng). Hành động: Phải có một bước lọc (filter) để loại bỏ các file có độ dài text thực tế bằng 0 trước khi đưa vào LangGraph.

- Thẻ <font'> (2.85 triệu thẻ): Số lượng khổng lồ này xác nhận việc lạm dụng thẻ inline để định dạng là cực kỳ phổ biến. Bước tag.unwrap() để nối chữ (như "Ủ y ban") trong hàm cleaner là bắt buộc.

## 2. Phân tích Cấu trúc (Structural Patterns)
- Từ khóa "Điều" (Trung bình 9.6 lần/file): Đây là "xương sống" của tập dữ liệu. Hầu hết các văn bản đều được chia thành các Điều (khoảng 10 Điều mỗi file).

- Từ khóa "Chương" (~30.000 file chứa nội dung này): Chỉ một phần tập dữ liệu (như Luật, Nghị định) mới có "Chương", còn lại (như Quyết định, Thông tư ngắn) thì không có.

## 3. Phân tích độ dài
- Phần lớn văn bản ngắn (~1037 từ), nhưng bị kéo lệch bởi một vài văn bản khổng lồ (tới 363,721 từ).
- Nhiễu (Noise): Có những file quá ngắn (14 từ) - chắc chắn là rác hoặc lỗi.