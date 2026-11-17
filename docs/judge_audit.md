# Judge audit

Audit dùng verdict replay trong hai CSV công khai. `FAIL` là lớp dương. Ngưỡng hiệu chuẩn là κ ≥ 0,60, precision ≥ 0,80 và recall ≥ 0,70.

| Tiêu chí | n | TP / FP / FN / TN | κ | Precision | Recall | Tỷ lệ FAIL quan sát → hiệu chỉnh | Kết quả |
|---|---|---|---|---|---|---|---|
| tone_ok | 100 | 24 / 4 / 6 / 66 | 0,757 | 0,857 | 0,800 | 28% → 30% | PASS. Dùng để chấm giọng điệu trên replay. |
| helpful | 100 | 9 / 0 / 21 / 70 | 0,375 | 1,000 | 0,300 | 9% → 30% | FAIL. Loại khỏi gate. |

## Bất đồng và cách sửa rubric

| Case | Judge | Người | Nhãn phù hợp | Bằng chứng và thay đổi rubric |
|---|---|---|---|---|
| H-008 | PASS | FAIL | Người | “Em”, “nha” và “check giúp em” tạo giọng quá suồng sã. Chấm cách xưng hô và ngữ vực của cả câu. |
| H-017 | PASS | FAIL | Người | Ghi chú xác định khách lớn tuổi. Thêm ví dụ về cách gọi “bạn ơi” với khách lớn tuổi và cung cấp ngữ cảnh khi chấm ca tương tự. |
| H-029 | PASS | FAIL | Người | “Không cần nhắn thêm” mang giọng ra lệnh. Chấm nội dung của từng câu, kể cả khi mở đầu có “Dạ” và “vui lòng”. |
| H-042 | FAIL | PASS | Người | Phản hồi lịch sự, đủ số tiền và thời gian nhận. Cho phép câu ngắn và chỉ yêu cầu xin lỗi khi ngữ cảnh có bất tiện cần ghi nhận. |
| H-051 | FAIL | PASS | Người | Từ “refund” được CS LogiX chấp nhận. Đưa thuật ngữ được phép vào rubric. |
| HL-015 | PASS | FAIL | Người | Reply ghi 55.000đ, ledger ghi 40.000đ. Kiểm tra số tiền bằng phép đối chiếu ledger trước khi chấm mức độ hữu ích. |
| HL-016 | PASS | FAIL | Người | Reply ghi 55.000đ, ledger ghi 35.000đ. Đặt sai lệch số tiền là lỗi bắt buộc kể cả khi lời xin lỗi lịch sự. |

## Quyết định

Judge `helpful` phát hiện 9 trong 30 lỗi theo nhãn người và bỏ sót 21 lỗi. Precision 1,000 chỉ phản ánh 9 verdict FAIL đều đúng. Recall 0,300 và κ 0,375 ở dưới ngưỡng, nên không dùng verdict `helpful` làm gate. Tỷ lệ hiệu chỉnh 30% là ước lượng tổng hợp, còn 21 verdict sai trên từng case vẫn giữ nguyên.

`tone_ok` đạt ba ngưỡng trên bộ replay công khai. Các chỉnh sửa rubric cần được kiểm lại bằng bộ held-out có nhãn người mới. Kiểm tra tính đúng của số tiền và approval bằng code dựa trên ledger.

```powershell
# Chạy từ src bằng Python trong .venv
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
```
