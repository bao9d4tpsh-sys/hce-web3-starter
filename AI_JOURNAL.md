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


