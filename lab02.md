# BÁO CÁO THỰC HÀNH LAB 02: VÍ VÀ GIAO DỊCH ĐẦU TIÊN
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Mục tiêu:** Nắm vững cấu trúc giao dịch, cơ chế tính phí gas, nguyên nhân thất bại ở tầng Client vs. tầng On-chain, và nguyên tắc kế toán / tuân thủ trong Web3.

---

## 1. Bảng đối chiếu giao dịch (Bước 3)

Dưới đây là bảng đối chiếu giữa giao dịch thành công và giao dịch thất bại trên mạng thử nghiệm **Sepolia Testnet**.

| Trường dữ liệu | Giao dịch thành công | Giao dịch thất bại (On-chain Reverted) | Giao dịch thất bại (Client-side / MetaMask chặn) |
| :--- | :--- | :--- | :--- |
| **Mã băm giao dịch (TxHash)** | `0xbf85d1b058d3acd41dca546a01990f5f7a86fae4c5877306051aea6ddbcff79f` *(hoặc mã băm cá nhân của bạn)* | `0xa365408fe04d15564e154e46d10b0d85395e28b2ed5e7695786d5e098ecdf8a6` | **Không có (N/A)** *(Bị chặn trước khi ký và phát sóng lên mạng P2P)* |
| **Số tiền chuyển (Value)** | `0.01 Sepolia ETH` *(Ví dụ mẫu: 0.00071184 ETH)* | `0.005277 ETH` *(Số tiền không bị trừ khỏi ví gửi, được hoàn lại nguyên vẹn)* | `0.01 Sepolia ETH` |
| **Phí giao dịch thực trả** | `0.0001383 ETH` *(21,000 gas × 6.5856 Gwei)* | `0.0001172 ETH` *(88,998 gas × 1.3169 Gwei)* **-> Vẫn bị trừ phí!** | `0 ETH` *(Chưa phát sinh giao dịch trên blockchain)* |
| **Trạng thái (Status)** | `Success (0x1)` / Confirmed | `Fail / Reverted (0x0)` | `Rejected / Blocked by Client` |
| **Nguyên nhân thất bại** | Không có (Giao dịch hợp lệ) | Lỗi logic thực thi hợp đồng (`Execution Reverted` / Hết gas / Vi phạm điều kiện require) | **Tình huống A:** Sai mã kiểm tra địa chỉ (`Checksum failed`).<br>**Tình huống B:** Số dư không đủ bù phí gas (`Insufficient funds for gas`). |

> **Ghi chú tra cứu Etherscan:**
> - Link tra cứu giao dịch thành công: [Sepolia Etherscan Tx Success](https://sepolia.etherscan.io/tx/0xbf85d1b058d3acd41dca546a01990f5f7a86fae4c5877306051aea6ddbcff79f)
> - Link tra cứu giao dịch thất bại on-chain: [Sepolia Etherscan Tx Failed](https://sepolia.etherscan.io/tx/0xa365408fe04d15564e154e46d10b0d85395e28b2ed5e7695786d5e098ecdf8a6)

---

## 2. Trả lời câu hỏi nghiệp vụ (Đúng 3 câu theo yêu cầu)

**Câu hỏi:** *Nếu bạn chuyển nhầm cho người lạ, có lấy lại được không? Vì sao?*

**Trả lời:**  
1. Nếu bạn chuyển nhầm tiền mã hóa cho một người lạ, bạn hoàn toàn không thể đơn phương lấy lại hoặc yêu cầu hệ thống thu hồi số tiền đó.  
2. Nguyên nhân là do mạng blockchain vận hành theo cơ chế đồng thuận phân tán với đặc tính bất biến (*immutability*), không tồn tại máy chủ tập trung hay đơn vị trung gian nào (như ngân hàng) có thẩm quyền đảo ngược giao dịch đã được xác nhận.  
3. Cơ hội duy nhất để thu hồi là chủ động liên hệ và phụ thuộc hoàn toàn vào sự tự nguyện chuyển trả của chủ sở hữu ví nhận (trừ trường hợp ví đó thuộc một sàn giao dịch tập trung có định danh KYC và có lệnh can thiệp tư pháp).

---

## 3. Phân tích dưới góc độ chuyên môn (Kế toán & Tuân thủ AML)

### 3.1. Bài học nghiệp vụ cho Kế toán tài sản số
- **Hạch toán chi phí giao dịch thất bại:** Trong giao dịch truyền thống, lệnh chuyển tiền không thành công thường không mất phí. Tuy nhiên trên blockchain, giao dịch thất bại ở tầng On-chain **vẫn tiêu tốn gas và bị trừ phí thật**. Thợ đào/Validator vẫn phải thực hiện tính toán để phát hiện lỗi, do đó kế toán phải ghi nhận phí này vào tài khoản chi phí hoạt động (*Transaction Fee Expense*), không được bỏ qua khi đối chiếu số dư sổ sách.
- **Tách biệt giá trị chuyển và phí gas:** Phí giao dịch luôn thanh toán bằng đồng tiền bản địa (*Native token* như ETH), độc lập với tài sản chuyển giao (dù chuyển ETH hay Token ERC-20).

### 3.2. Bài học nghiệp vụ cho Chuyên viên Tuân thủ (AML / KYC)
- **Cơ chế Checksum (EIP-55):** Địa chỉ ví Ethereum có các chữ cái viết hoa/viết thường đại diện cho mã kiểm tra băm Keccak-256. Nếu người dùng gõ sai 1 ký tự, mã checksum sẽ không khớp, giúp phần mềm ví chặn đứng lỗi đánh máy.
- **Rủi ro chuyển nhầm địa chỉ hợp lệ:** Checksum chỉ xác thực tính toàn vẹn cú pháp của địa chỉ, **không thể xác thực danh tính chủ sở hữu**. Nếu chuyển nhầm sang một địa chỉ hợp lệ khác hoặc địa chỉ hợp đồng không có hàm rút tiền, dòng tiền sẽ bị phong tỏa vĩnh viễn (black hole).

---

## 4. Đặc tả nghiệp vụ mở rộng (SPEC v0.2 - Chống rủi ro chuyển tiền)

Để đạt mức đánh giá xuất sắc (Mức Giỏi), nhóm bổ sung đặc tả nghiệp vụ phòng ngừa gian lận và sai sót:

- **R1 (Kiểm tra Checksum):** Hệ thống giao diện bắt buộc chuẩn hóa địa chỉ qua hàm băm EIP-55 trước khi tạo giao dịch.
- **R2 (Cảnh báo số dư dự phòng gas):** Khi người dùng chọn "Max", hệ thống phải tự động giữ lại tối thiểu `0.002 ETH` cho phí gas, không cho phép gửi 100% số dư ETH.
- **R3 (Whitelist / Danh bạ an toàn):** Với giao dịch có giá trị lớn hơn 0.5 ETH, bắt buộc địa chỉ người nhận phải nằm trong danh sách đã xác minh trước đó hoặc yêu cầu chuyển thử một lượng nhỏ (dust transfer) để kiểm tra.
- **R4 (Kiểm tra địa chỉ Hợp đồng thông minh):** Cảnh báo người dùng nếu địa chỉ nhận là Contract Address không có khả năng nhận ETH để tránh việc khóa chết tài sản.

---

## 5. Nhật ký làm việc với AI (AI_JOURNAL)

### Lần 1
- **Prompt:** *"Viết bảng đối chiếu giao dịch thành công và thất bại cho Lab 2, giải thích tại sao chuyển toàn bộ tiền thì thất bại."*
- **AI trả về:** AI giải thích rằng giao dịch thất bại do số tiền chuyển bị trừ hết và phí giao dịch bị trừ âm, đồng thời nói giao dịch chuyển sai địa chỉ có thể liên hệ tổng đài MetaMask để hủy.
- **Đánh giá:** ❌ Sai, bỏ phần giải thích về hủy giao dịch.
- **Chỗ sai:**  
  1. AI nhầm lẫn MetaMask là tổ chức trung gian có quyền đảo ngược giao dịch (Blockchain là phi tập trung, không ai hủy được giao dịch đã confirm).  
  2. AI không phân biệt được lỗi chặn ở Client (không sinh TxHash, 0 phí) và lỗi On-chain Reverted (có TxHash, vẫn mất phí gas).
- **Cách sửa:** Sinh viên hiệu chỉnh lại nội dung: khẳng định tính bất biến của blockchain; tách rõ 2 tầng thất bại (Client-side vs On-chain); bổ sung dữ liệu thực nghiệm kiểm chứng từ Sepolia Etherscan.
- **Ai phát hiện:** Sinh viên phát hiện.
