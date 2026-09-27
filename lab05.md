# BÁO CÁO THỰC HÀNH LAB 05: VIẾT ĐẶC TẢ CHO CÔNG CỤ PHÂN TÍCH DÒNG TIỀN
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Kho lưu trữ GitHub:** [https://github.com/bao9d4tpsh-sys/hce-web3-starter](https://github.com/bao9d4tpsh-sys/hce-web3-starter)  
**Tệp đặc tả nghiệp vụ chính:** [`SPEC.md`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md)  
**Nguyên tắc cốt lõi:** **KHÔNG VIẾT MÃ NGUỒN TRONG BUỔI NÀY** — Tập trung 100% vào kỹ năng phân tích nghiệp vụ (BA) và hoàn thiện tài liệu đặc tả trước khi lập trình.

---

## 1. Tóm tắt nội dung đặc tả trong tệp [SPEC.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md)

Nhóm đã hoàn thành bản đặc tả chi tiết [SPEC.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md) với 6 phần cốt lõi:
1. **Mục đích:** Xây dựng công cụ phân tích dòng tiền vào/ra và biểu đồ số dư trong 90 ngày cho ví Ethereum phục vụ công tác kế toán và kiểm toán tuân thủ.
2. **Đầu vào:** `wallet_address` (42 ký tự hex), `ETHERSCAN_API_KEY` (đọc qua biến môi trường theo chuẩn `AGENTS.md`), `days` (mặc định 90 ngày).
3. **Quy tắc nghiệp vụ:** Bao gồm 6 quy tắc nền tảng (R1 đến R6) và **3 quy tắc mở rộng** (R7: Giao dịch tự chuyển ví; R8: Thuật toán xác định số dư gốc đầu kỳ; R9: Kiểm soát giới hạn tốc độ Rate Limit API).
4. **Đầu ra:** Bảng dữ liệu chi tiết từng dòng tiền, biểu đồ đường số dư lũy kế, và 3 chỉ số tài chính (Tổng vào, Tổng ra, Số dư cuối kỳ).
5. **Trường hợp ngoại lệ:** E1 (Danh sách rỗng), E2 (Lỗi xác thực API Key), E3 (Phân trang khi vượt 10.000 giao dịch), E4 (Địa chỉ sai cú pháp), E5 (Giao dịch tạo hợp đồng có `to == null`).
6. **Ngoài phạm vi:** Không phân tích token ERC-20, không quy đổi tiền pháp định VND/USD.

---

## 2. Biên bản kiểm tra chéo với nhóm bạn (Bước 3)

**Nhóm thực hiện đặc tả:** Nhóm K58 — Sinh viên: Bao (`bao9d4tpsh-sys`)  
**Nhóm kiểm tra chéo & phản biện:** Nhóm bạn đối ứng (Nhóm 02)  
**Nội dung phản biện:** Nhóm bạn đã đọc kỹ bản nháp v0.1 và chỉ ra **3 điểm mơ hồ** cần làm rõ:

---

### Điểm mơ hồ 1: Mốc bắt đầu của biểu đồ số dư lũy kế (Baseline Balance)
- **Nhóm bạn phát hiện:** Bản nháp ban đầu chỉ ghi *"vẽ biểu đồ số dư lũy kế theo thời gian"*. Nhóm bạn đặt câu hỏi: *"Nếu chỉ tính tổng dòng tiền trong 90 ngày thì điểm bắt đầu của trục tung $Y$ là 0 ETH hay là số dư thực tế của ví tại thời điểm cách đây 90 ngày? Nếu bắt đầu từ 0 thì số dư hiển thị có thể bị âm (nếu đầu kỳ ví có sẵn tiền và trong kỳ chỉ thực hiện rút ra)!"*
- **Đánh giá mức độ:** Rất nghiêm trọng (làm sai lệch hoàn toàn ý nghĩa tài chính của đồ thị số dư).
- **Cách nhóm đã sửa lại trong [SPEC.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md):**  
  Đã bổ sung **Quy tắc nghiệp vụ R8**: Trước khi vẽ đồ thị, chương trình phải gọi endpoint `eth_getBalance` để lấy số dư thực tế hiện tại, sau đó tính ngược lại số dư đầu kỳ bằng công thức:  
  $$\text{Số dư đầu kỳ} = \text{Số dư hiện tại} - \text{Tổng vào} + \text{Tổng ra (gồm phí)}$$  
  Đảm bảo trục tung của biểu đồ luôn phản ánh đúng số dư thực tế trong ví của người dùng.

---

### Điểm mơ hồ 2: Giao dịch tự chuyển ví cho chính mình (Self-Transfer) & Gọi Contract không có Value
- **Nhóm bạn phát hiện:** Bản nháp ghi *"giao dịch có to là địa chỉ ví thì tính là vào, from là địa chỉ ví thì tính là ra"*. Nhóm bạn hỏi: *"Nếu một giao dịch có `from == to` (người dùng tự chuyển tiền cho chính mình hoặc tương tác kích hoạt chức năng) thì hệ thống tính cả vào lẫn ra hay xử lý thế nào? Tiền chuyển không đổi nhưng phí gas thì sao?"*
- **Đánh giá mức độ:** Gây trùng lặp số liệu doanh thu / chi phí ảo trong hạch toán kế toán.
- **Cách nhóm đã sửa lại trong [SPEC.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md):**  
  Đã bổ sung **Quy tắc nghiệp vụ R7**: Trường hợp `from == to`, số tiền chuyển `value` được xem là biến động nội bộ (net effect = 0), không cộng dồn vào dòng tiền vào hay dòng tiền ra; riêng phần phí gas (`gasUsed * gasPrice`) được phân loại rõ ràng là một khoản chi phí độc lập (`FEE_ONLY`) và tính vào dòng tiền ra.

---

### Điểm mơ hồ 3: Giới hạn tốc độ truy vấn API (Rate Limit) khi phân trang
- **Nhóm bạn phát hiện:** Bản nháp ghi *"nếu ví có hơn 10.000 giao dịch thì phải lấy đủ các trang"*, nhưng không nói rõ cơ chế gửi request. Etherscan gói miễn phí giới hạn 5 requests/giây. Nếu gửi vòng lặp phân trang liên tục thì API sẽ trả mã lỗi 429 và chương trình sẽ bị ngắt đột ngột.
- **Cách nhóm đã sửa lại trong [SPEC.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md):**  
  Đã bổ sung **Quy tắc nghiệp vụ R9** và cập nhật ngoại lệ **E3**: Cài đặt độ trễ tối thiểu 0.25 giây giữa mỗi trang truy vấn, đồng thời bổ sung cơ chế kiểm tra mã trạng thái HTTP trước khi xử lý dữ liệu theo đúng quy ước `AGENTS.md`.

---

## 3. Bài học rút ra cho Chuyên viên Phân tích Nghiệp vụ (BA)

1. **Nguyên tắc "Không để AI tự đoán":** Nếu tài liệu đặc tả mơ hồ một chi tiết nhỏ (như số dư đầu kỳ hay giao dịch thất bại), công cụ AI lập trình ở Lab 06 sẽ tự động đoán theo hướng dễ nhất (gán số dư bắt đầu bằng 0, bỏ qua phí của giao dịch fail), dẫn đến việc sinh ra phần mềm sai lệch về mặt kế toán tài chính.
2. **Giá trị của Kiểm tra chéo (Peer Review):** Người viết đặc tả thường bị rơi vào "điểm mù" do tự cho rằng các logic ngầm định là hiển nhiên. Việc đổi tài liệu cho một nhóm khác đọc sẽ bộc lộ ngay lập tức các lỗ hổng logic nghiệp vụ trước khi bước vào giai đoạn tốn kém chi phí nhất là viết mã nguồn.
