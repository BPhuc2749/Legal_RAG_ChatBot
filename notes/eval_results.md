# Mini Eval - Week 1 Day 5

## Setup
- TOP_K: 5
- Model: gemini-2.5-flash-lite
- Embedding: bkai-foundation-models/vietnamese-bi-encoder
- Data: 7 PDFs (law + policy)

## Results

### Q1: Các hành vi bị nghiêm cấm về an ninh mạng?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)


### Q2: Hành vi xâm phạm an ninh mạng là gì?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)


### Q3: Thông tin trên không gian mạng gồm những loại nào?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời cho ra có ý đúng nhưng chưa đủ )
- Notes: Tăng top-k

### Q4: Các nguyên tắc bảo vệ thông tin cá nhân trên mạng là gì ?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)


### Q5: Các nguyên tắc bảo vệ dữ liệu cá nhân là gì ?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)


### Q6: Việc xóa, hủy dữ liệu cá nhân được thực hiện trong trường hợp nào ?
- Retrieval: ❌ (chưa cho chunk đúng theo mong muốn, còn nhiều chunk nhiễu)
- Answer: ❌ (câu trả lời có ý đúng nhưng chưa cho ra kết quả tốt)
- Notes: tăng top-k

### Q7: Các hành vi bị nghiêm cấm trong giao dịch điện tử ?
- Retrieval: ✅ (chunk liệt kê điều cấm xuất hiện trong top-k; LUẬT GIAO DỊCH ĐIỆN TỬ trang 2–3)
- Answer: ✅ (liệt kê 8 ý, có nguồn)
- Notes: Prompt ép format + tăng k giúp giảm bỏ sót

### Q8: Quyền của chủ thể cá nhân dữ liệu là gì ?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)

### Q9: Nghĩa vụ của chủ thể cá nhân dữ liệu là gì ?
- Retrieval: ✅ (các chunk đôi khi bị nhiễu nhưng vẫn cho ra chunk cần thiết)
- Answer: ✅ (câu trả lời khá ổn)

### Q10: Dữ liệu sinh trắc học có phải dữ liệu nhạy cảm không?
- Retrieval: ✅ (cho chunk tốt, có liên quan)
- Answer: ✅ (câu trả lời nêu rõ ý , có dẫn chứng trong file gốc)



### Q11: Khi nào được xử lý dữ liệu cá nhân mà không cần sự đồng ý?
- Retrieval: ✅(cho ra chunk có liên quan , còn có nhiễu)
- Answer: ✅ (còn bị mix bởi nhiều nhiễu, nhìn chung vẫn có ý đúng nhưng thiếu)


