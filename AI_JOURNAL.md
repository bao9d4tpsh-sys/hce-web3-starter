# NHẬT KÝ LÀM VIỆC VỚI AI — ECO2432

---

## Lab 04: Nhận diện hợp đồng có rủi ro

### Lần 1 — Thẩm định hợp đồng token với vai trò Chuyên viên Thẩm định rủi ro
**Prompt (dán nguyên văn):**
```text
Bạn là chuyên viên thẩm định rủi ro tài sản số.
Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà
chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
- Tên hàm và số dòng
- Người nắm giữ token chịu rủi ro gì
Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.

[Mã nguồn contracts/lab04/ClubTokens.sol gồm ClubTokenA, ClubTokenB, ClubTokenC]
```

**AI trả về (tóm tắt):**
- ClubTokenA: Không có quyền đặc biệt nào của chủ sở hữu. Tuy nhiên AI ban đầu nhận định là "thiếu an toàn do không có cơ chế quản trị Ownable để can thiệp khi gặp sự cố".
- ClubTokenB: Nhận diện hàm `mint(address to, uint256 amount)` tại dòng 18–20 cho phép `onlyOwner` tạo thêm token vô hạn, gây rủi ro pha loãng giá trị (lạm phát vô hạn / Rug Pull).
- ClubTokenC: Nhận diện hàm `setRestricted(address user, bool status)` tại dòng 30–32 và hàm `_update` tại dòng 34–37 cho phép `onlyOwner` cấm địa chỉ chuyển token (`!restricted[from]`).

**Đánh giá:** ⚠️ Phải sửa phần phân tích ClubTokenA.

**So sánh kết quả giữa Đọc thủ công và AI:**
1. **Đọc thủ công tìm ra gì (15 phút đầu):**
   - ClubTokenA: Không có biến `owner`, không có hàm `mint` bổ sung, tổng cung 1 triệu bất biến.
   - ClubTokenB: Phát hiện dòng 18 có `mint` với `onlyOwner`, nhận diện ngay nguy cơ lạm phát vô hạn.
   - ClubTokenC: Phát hiện dòng 30 `setRestricted` và dòng 35 `require(!restricted[from])`. Phát hiện ví bị hạn chế thì không chuyển được.
2. **AI tìm thêm được gì:**
   - AI làm rõ cơ chế bất đối xứng của ClubTokenC: chiều nhận (`to`) không bị chặn, chỉ chặn chiều gửi (`from`). Đây chính là mô hình bẫy **Honeypot** kinh điển (nạn nhân mua được trên DEX nhưng không bao giờ bán lại được).
   - AI chỉ ra thêm việc ClubTokenB không có bất kỳ giới hạn trần tổng cung (`cap`) hay sự kiện chuyên biệt nào để cảnh báo cộng đồng.
3. **Chỗ AI nói sai và cách sửa:**
   - *Chỗ sai:* AI suy luận theo lối mòn của phần mềm truyền thống: cho rằng ClubTokenA có rủi ro bảo mật vì "không có ai làm chủ sở hữu quản lý".
   - *Cách sửa:* Sinh viên hiệu chỉnh lại: trong hợp đồng thông minh Web3, một token phi tập trung hoàn toàn (không có `Ownable`, không có backdoor) mới là mức độ an toàn tối thượng trước sự can thiệp của bên thứ ba.
   - *Ai phát hiện:* **Sinh viên phát hiện.**

---

## Lab 06: Sinh mã bằng AI và kiểm tra kết quả

### Lần 1 — Yêu cầu AI sinh mã Python phân tích dòng tiền từ SPEC.md
**Prompt (dán nguyên văn):**
```text
Đọc tệp SPEC.md trong dự án và viết chương trình Python thực hiện đúng đặc tả đó.
Tuân thủ các quy ước trong AGENTS.md.
Trước khi viết mã, tóm tắt lại cách bạn hiểu yêu cầu để tôi xác nhận.
```

**AI trả về (tóm tắt):**
- Tóm tắt cách hiểu các quy tắc dòng tiền vào/ra cơ bản.
- Sinh ra đoạn mã Python dùng thư viện `requests` để lấy giao dịch từ Etherscan và vẽ đồ thị `matplotlib`.

**Đánh giá:** ⚠️ Phải sửa (Phát hiện 3 lỗi nghiêm trọng trong danh mục 6 điểm kiểm tra bắt buộc).

---

### Bảng rà soát 6 điểm kiểm tra bắt buộc (Checklist Lab 06)

| # | Hạng mục kiểm tra | Cách kiểm tra | Kết quả mã AI sinh ra ban đầu | Đánh giá & Cách khắc phục | Ai phát hiện |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Đơn vị tiền** | Kiểm tra số dư hiển thị có chia $10^{18}$ không | ✅ Đã chia cho $10^{18}$ để đổi từ Wei sang ETH. | Đạt yêu cầu. | AI tự nhận |
| **2** | **Khóa API** | Tìm chuỗi khóa API trong mã nguồn | ❌ AI khởi tạo biến: `ETHERSCAN_API_KEY = "YourApiKeyTokenHere"` ghi cứng trong mã. | **Vi phạm quy tắc bảo mật `AGENTS.md`.** Sinh viên sửa lại: dùng `os.environ.get("ETHERSCAN_API_KEY")` để đọc từ biến môi trường. | **Sinh viên phát hiện** |
| **3** | **Phân trang** | Kiểm tra ví có nhiều hơn 10.000 tx | ⚠️ AI chỉ gọi 1 request với `offset=10000`, không có vòng lặp `while True` với `page += 1`. | Thiếu dữ liệu nếu ví có nhiều giao dịch. Sinh viên bổ sung vòng lặp phân trang tự động. | **Sinh viên phát hiện** |
| **4** | **Giao dịch thất bại** | Có tính phí gas của giao dịch thất bại không | ❌ AI viết: `if tx['isError'] == '0': ... else: continue` $\rightarrow$ Bỏ qua hoàn toàn giao dịch lỗi! | **Lỗi nghiệp vụ tài chính nghiêm trọng:** Giao dịch lỗi tuy không chuyển được tiền nhưng **vẫn bị trừ phí gas**. Sinh viên sửa lại: thêm nhánh `FAILED_FEE`, cộng phí gas của giao dịch lỗi vào dòng tiền ra (`total_outflow`). | **Sinh viên phát hiện** |
| **5** | **Xử lý lỗi** | Thử nhập API key sai hoặc ngắt mạng | ❌ Chương trình crash với lỗi `KeyError: 'result'` do không kiểm tra `status == "1"`. | **Vi phạm quy tắc `AGENTS.md`.** Sinh viên bổ sung bước kiểm tra mã phản hồi HTTP (`status == 200`) và mã trạng thái JSON của Etherscan trước khi đọc trường `result`. | **Sinh viên phát hiện** |
| **6** | **Phiên bản API** | Đối chiếu tài liệu Etherscan hiện hành | ⚠️ AI dùng endpoint v1 cũ và không có độ trễ giữa các trang truy vấn, gây lỗi HTTP 429 khi vượt 5 req/s. | Sinh viên cập nhật endpoint chuẩn `api-sepolia.etherscan.io`, thêm `time.sleep(0.25)` giữa các trang truy vấn để tuân thủ Rate Limit. | **Sinh viên phát hiện** |

### Tổng kết bài học Lab 06:
- Tỷ lệ lỗi AI mắc phải: 3 lỗi sai/thiếu nghiêm trọng (Khóa API, Giao dịch thất bại, Xử lý lỗi).
- Bài học cốt lõi: AI có thể gõ cú pháp rất nhanh, nhưng **lỗi logic nghiệp vụ tài chính** (như bỏ quên phí gas của giao dịch thất bại) chỉ có con người am hiểu sâu sắc quy tắc kinh tế mới phát hiện và chấn chỉnh được.



