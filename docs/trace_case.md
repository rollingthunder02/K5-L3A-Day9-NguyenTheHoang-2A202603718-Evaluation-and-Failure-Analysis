# Trace case — C-002@11

Chạy từ `src/` bằng `python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11` rồi chạy lại với `--shape fixed`.

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11` và `fixed C-002@11`, replay trực tiếp bằng CLI |
| Triệu chứng | Ledger ghi 1 khoản hoàn 20.000đ, trong khi nhãn yêu cầu 0 khoản và 0đ. Reply xác nhận đã hoàn. Grader Lab 8 báo `status resolved != denied`. |
| Bước sai đầu tiên | Event 3, `model_override`, payload `{"delay_days": 5}`. |
| Vì sao là bước đầu tiên | Event 1 chuyển giao với phạm vi tra cứu của chủ đơn. Event 2 tìm đúng đơn O-202. Event 3 thay dữ liệu tra cứu bằng số ngày do ticket khai. Event 4 dùng số đó để báo giá 20.000đ. |
| Failure mode | FM-03 — ticket_trust |
| Đối chứng | Event 3 của `fixed` là `quote` với `amount_vnd=0` và `reason=no_entitlement`. Kết quả `denied`, ledger 0đ, grader PASS. |
| Regression test | `tests/test_lab9_trace_case.py::test_ticket_claim_cannot_override_order_delay` kiểm tra trạng thái, số tiền và số lần hoàn từ ledger. `seeded_regression` là đối chứng lỗi với `xfail(strict=True)`. |
| Giới hạn | Replay xác nhận kết quả với seed 11. Chưa có run ID của report M4 và chưa đo tần suất lỗi trên các seed khác. |
