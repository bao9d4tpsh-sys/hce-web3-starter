# ĐẶC TẢ YÊU CẦU NGHIỆP VỤ (SPEC.md)
## DỰ ÁN: CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ON-CHAIN (ETH CASH FLOW ANALYZER)
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432) — Lab 05  
**Vai trò thực hiện:** Chuyên viên Phân tích Nghiệp vụ (Business Analyst - BA)  
**Phiên bản:** v1.0 (Đã hoàn thiện qua kiểm tra chéo)

---

## 1. Mục đích
Xây dựng một công cụ bằng Python nhận vào một địa chỉ ví Ethereum, tự động truy vấn dữ liệu sổ cái từ Etherscan API và trích xuất báo cáo phân tích dòng tiền vào/ra kèm biểu đồ biến động số dư lũy kế trong 90 ngày gần nhất phục vụ chuyên viên phân tích nghiệp vụ, kiểm toán tuân thủ (AML) và kế toán tài sản số.

---

## 2. Đầu vào
1. **Địa chỉ ví mục tiêu (`wallet_address`):**
   - Định dạng chuỗi 42 ký tự thập lục phân bắt đầu bằng `0x`.
   - Có kiểm tra tính hợp lệ cú pháp (EIP-55 checksum hoặc chuỗi hex 20 bytes).
   - Do người dùng cung cấp qua tham số dòng lệnh (`--address`) hoặc nhập từ bàn phím.
2. **Khóa API Etherscan (`api_key`):**
   - Đọc tự động từ biến môi trường `ETHERSCAN_API_KEY`.
   - Tuyệt đối không ghi cứng khóa API trong mã nguồn (tuân thủ quy tắc bảo mật `AGENTS.md`).
3. **Khoảng thời gian phân tích (`days`):**
   - Số nguyên dương biểu diễn số ngày tính ngược từ thời điểm hiện tại.
   - Giá trị mặc định là **90 ngày**.

---

## 3. Quy tắc nghiệp vụ (Business Rules)

- **R1 (Dòng tiền vào - Inflow):** Giao dịch có trường `to` trùng khớp với địa chỉ ví đang xét (so sánh không phân biệt chữ hoa/chữ thường) và trạng thái thành công (`isError == "0"`) được ghi nhận là dòng tiền vào. Giá trị dòng tiền vào chính bằng số tiền chuyển (`value`).
- **R2 (Dòng tiền ra - Outflow):** Giao dịch có trường `from` trùng khớp với địa chỉ ví đang xét và trạng thái thành công (`isError == "0"`) được ghi nhận là dòng tiền ra.
- **R3 (Chi phí thực tế của lệnh chuyển đi):** Với mỗi giao dịch chuyển tiền ra thành công, số tiền thực tế bị trừ khỏi ví được tính bằng:
  $$\text{Số tiền thực trừ} = \text{Giá trị chuyển (value)} + \text{Phí giao dịch (gasUsed} \times \text{gasPrice)}$$
- **R4 (Xử lý giao dịch thất bại):** Giao dịch xuất phát từ ví (`from` trùng địa chỉ ví) nhưng có trạng thái thất bại (`isError == "1"`):
  - Giá trị chuyển (`value`) không bị trừ (hoàn lại nguyên vẹn).
  - **Phí giao dịch vẫn bị trừ khỏi ví** và bắt buộc phải hạch toán vào dòng tiền ra.
- **R5 (Chuẩn hóa đơn vị đo lường):** Mọi giá trị số tiền nhận về từ API (`value`, `gasPrice`) đều ở đơn vị Wei. Chương trình bắt buộc phải chia cho $10^{18}$ trước khi tính toán số dư và hiển thị ra giao diện/báo cáo.
- **R6 (Trình tự thời gian):** Toàn bộ dữ liệu giao dịch thu thập được phải được sắp xếp theo mốc thời gian (`timeStamp`) tăng dần (từ cũ nhất đến mới nhất) trước khi tính toán số dư lũy kế theo chuỗi thời gian.
- **R7 (Quy tắc bổ sung 1 — Giao dịch tự chuyển Self-Transfer):** Nếu giao dịch có trường `from` trùng với trường `to` (ví tự gửi cho chính mình):
  - Giá trị chuyển `value` không làm biến động số dư tài sản.
  - Phí giao dịch vẫn bị trừ và được ghi nhận là một khoản chi phí độc lập.
- **R8 (Quy tắc bổ sung 2 — Xác định số dư gốc đầu kỳ):** Để biểu đồ số dư lũy kế phản ánh đúng số dư thực tế của ví tại mọi thời điểm, số dư đầu kỳ (ngày thứ 90 trước) được xác định bằng:
  $$\text{Số dư đầu kỳ} = \text{Số dư hiện tại (eth\_getBalance)} - \sum (\text{Dòng tiền vào}) + \sum (\text{Dòng tiền ra gồm phí})$$
- **R9 (Quy tắc bổ sung 3 — Kiểm soát tốc độ gọi API / Rate Limit):** Để tuân thủ chính sách API Etherscan gói miễn phí (tối đa 5 requests/giây), chương trình phải cài đặt cơ chế nghỉ tối thiểu 0.25 giây giữa các lượt gọi phân trang hoặc tự động thử lại khi gặp mã trạng thái HTTP 429.

---

## 4. Đầu ra
1. **Bảng dữ liệu dòng tiền chi tiết (Dạng bảng Console hoặc xuất file CSV):**
   - Các cột hiển thị: `Thời gian (UTC)`, `Mã băm (TxHash rút gọn)`, `Loại dòng tiền (IN / OUT / FAILED_FEE)`, `Số tiền chuyển (ETH)`, `Phí giao dịch (ETH)`, `Số dư lũy kế (ETH)`.
2. **Biểu đồ đường biến động số dư (Line Chart):**
   - **Trục ngang (X):** Thời gian (ngày/tháng trong 90 ngày).
   - **Trục dọc (Y):** Số dư lũy kế của ví (đơn vị ETH).
   - Biểu đồ thể hiện trực quan các mốc tăng (nạp tiền) và giảm (rút tiền / trả phí gas).
3. **Ba con số chỉ số tài chính tổng hợp (Summary KPIs):**
   - **Tổng dòng tiền vào:** Tổng lượng ETH nạp vào trong kỳ.
   - **Tổng dòng tiền ra:** Tổng lượng ETH chuyển đi cộng dồn toàn bộ phí gas thực tế.
   - **Số dư cuối kỳ:** Số dư khả dụng tại thời điểm kết thúc kỳ phân tích.

---

## 5. Trường hợp ngoại lệ (Edge Cases)
- **E1 (Danh sách rỗng):** Nếu API trả về mảng giao dịch rỗng (`result: []`), in thông báo: `"Vi khong co giao dich trong ky"`, không báo lỗi crash chương trình, hiển thị tổng thu/chi bằng 0.
- **E2 (Lỗi API Key hoặc endpoint):** Nếu API trả về `status: "0"` kèm thông báo lỗi (ví dụ: `Invalid API Key`), in mã lỗi chi tiết và hướng dẫn cấu hình biến môi trường, sau đó dừng chương trình an toàn.
- **E3 (Ví có trên 10.000 giao dịch):** Etherscan giới hạn 10.000 bản ghi mỗi truy vấn. Chương trình phải kích hoạt cơ chế phân trang tự động (`page`, `offset`) để lấy đầy đủ toàn bộ giao dịch trong khung thời gian 90 ngày.
- **E4 (Địa chỉ ví không hợp lệ):** Nếu địa chỉ người dùng nhập không đúng định dạng (độ dài khác 42 ký tự hoặc ký tự không hợp lệ), chương trình báo lỗi cú pháp ngay lập tức và từ chối gửi request.
- **E5 (Giao dịch khởi tạo hợp đồng):** Giao dịch tạo hợp đồng thông minh có trường `to` rỗng (`null` hoặc `""`). Chương trình phải xử lý an toàn không để phát sinh lỗi `NoneType` khi so sánh địa chỉ.

---

## 6. Ngoài phạm vi (Out of Scope)
- Không phân tích các giao dịch Token ERC-20, ERC-721, ERC-1155 (chỉ tập trung vào đồng ETH gốc).
- Không tự động quy đổi giá trị sang tiền pháp định VND hoặc USD.
- Không thực hiện các thao tác ghi dữ liệu hoặc can thiệp chuyển tiền (chỉ là công cụ phân tích dữ liệu đọc).
