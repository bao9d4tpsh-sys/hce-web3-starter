# BÁO CÁO THỰC HÀNH LAB 03: ĐỌC GIAO DỊCH VÀ HỢP ĐỒNG TRÊN ETHERSCAN
**Tệp nộp bài:** `forensics.md`  
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Mục tiêu:** Mổ xẻ 10 trường dữ liệu cốt lõi của giao dịch on-chain phục vụ nghiệp vụ Kế toán/Tuân thủ (AML); phân biệt Bytecode và Verified Source Code; phân tích hàm Đọc/Ghi và cơ chế kiểm soát tập trung (Blacklist/Freeze) trong các hợp đồng tiền ổn định giá (USDT, USDC).

---

## PHẦN 1: MỔ XẺ GIAO DỊCH ON-CHAIN (BƯỚC 1)

**Mã băm giao dịch phân tích (TxHash):**  
`0xbf85d1b058d3acd41dca546a01990f5f7a86fae4c5877306051aea6ddbcff79f`  
*(Đường dẫn tra cứu: [Sepolia Etherscan Tx Details](https://sepolia.etherscan.io/tx/0xbf85d1b058d3acd41dca546a01990f5f7a86fae4c5877306051aea6ddbcff79f))*

### Bảng phân tích 10 trường dữ liệu giao dịch

| # | Tên trường | Giá trị thực tế trên Etherscan | Ý nghĩa kỹ thuật | Vì sao người làm nghiệp vụ (Kế toán / AML) cần |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Status** | `Success (0x1)` | Cho biết trạng thái thực thi giao dịch thành công hay thất bại. | **Rất quan trọng trong kế toán:** Giao dịch dù thất bại (`Fail/Reverted`) trên blockchain **vẫn bị trừ phí gas**. Kế toán phải hạch toán chi phí này vào chi phí hoạt động dù không chuyển được tiền. |
| **2** | **Block** | `11794648` *(1 block confirmation)* | Số thứ tự của khối trên blockchain chứa giao dịch này. | **Xác định tính hữu hiệu và thời điểm ghi nhận:** Càng nhiều block xác nhận phía sau thì giao dịch càng bất khả đảo ngược (tránh rủi ro Reorg / Double spending). |
| **3** | **Timestamp** | `1790527968`<br>(2026-09-27 16:52:48 UTC) | Dấu thời gian Unix khi validator đóng khối thành công. | **Mốc ghi nhận kế toán & quy đổi tỷ giá:** Là căn cứ xác định kỳ kế toán (ngày/tháng/năm) và lấy tỷ giá hối đoái tham chiếu (ví dụ ETH/USD hoặc ETH/VND tại thời điểm phát sinh) để ghi nhận doanh thu/chi phí theo luật thuế. |
| **4** | **From / To** | **From:** `0x113b614b6a21f5ec532a4cf4d71dfa8fe68be688`<br>**To:** `0xdeadc0dec18f9f380c7c272e366a5e0b32aa1eff` | Địa chỉ ví người gửi (`From`) và địa chỉ ví người nhận hoặc hợp đồng (`To`). | **Xác minh danh tính (KYC/AML):** Đối chiếu với cơ sở dữ liệu các ví nghi vấn, địa chỉ bị trừng phạt (OFAC), hoặc ví sàn giao dịch để truy vết dòng tiền bất hợp pháp. |
| **5** | **Value** | `0.00071184311448282 ETH`<br>(711,843,114,482,820 Wei) | Giá trị tài sản gốc (ETH) được chuyển giao giữa hai địa chỉ. | **Giá trị giao dịch gốc:** Số tiền thanh toán chuyển khoản, căn cứ tính thuế giá trị gia tăng hoặc thuế thu nhập chuyển nhượng tài sản mã hóa. |
| **6** | **Transaction Fee** | `0.000138298435695 ETH` | Chi phí thực trả cho mạng lưới: $\text{Fee} = \text{Gas Used} \times \text{Effective Gas Price}$. | **Chi phí giao dịch:** Chi phí hoạt động của doanh nghiệp cần hạch toán riêng vào tài khoản chi phí tài chính / phí mạng lưới. |
| **7** | **Gas Price** | `6.585639795 Gwei`<br>(0.0000000065856... ETH) | Đơn giá cho mỗi đơn vị gas tại thời điểm giao dịch được đóng khối. | **Giải thích biến động chi phí:** Giúp nhà quản trị giải thích tại sao cùng một loại giao dịch mà giờ cao điểm phí cao gấp nhiều lần giờ thấp điểm. |
| **8** | **Gas Limit** | `21,000` | Lượng gas tối đa mà ví người gửi cấp phép cho giao dịch tiêu thụ. | **Quản trị rủi ro thất bại:** Nếu người dùng/ứng dụng cấu hình gas limit quá thấp, giao dịch sẽ bị lỗi `Out of Gas` $\rightarrow$ giao dịch thất bại nhưng **vẫn mất toàn bộ phí** đã cấp. |
| **9** | **Gas Used** | `21,000` (100% Limit) | Lượng công việc tính toán thực tế mà EVM đã tiêu tốn. | Với chuyển ETH thuần túy, gas tiêu chuẩn luôn là `21,000`. Khi $\text{Gas Used} = \text{Gas Limit}$, đây là dấu hiệu nhận diện giao dịch bị cạn gas (`Out of Gas`). |
| **10** | **Nonce** | `1` | Số thứ tự giao dịch xuất phát từ địa chỉ ví gửi (bắt đầu từ 0). | **Kiểm soát tính tuần tự & phát hiện gian lận:** Nonce ngăn chặn tấn công phát lại (*replay attack*). Giúp chuyên viên phát hiện giao dịch bị kẹt (pending) hoặc giao dịch bị thay thế (speed up / cancel). |

---

## PHẦN 2: PHÂN BIỆT MÃ MÁY, MÃ NGUỒN VÀ LOẠI HÀM (BƯỚC 2)

### 1. Phân biệt Bytecode và Verified Source Code
- **Bytecode (Mã máy):** Là chuỗi ký tự Hexadecimal (ví dụ: `0x608060405234801561001057600080fd5b50...`) được máy ảo EVM đọc và thực thi. Con người không thể đọc trực tiếp các quy tắc nghiệp vụ từ bytecode. Mọi hợp đồng triển khai trên Ethereum đều có bytecode.
- **Verified Source Code (Mã nguồn đã xác thực):** Là mã nguồn viết bằng ngôn ngữ bậc cao (như Solidity) do nhà phát triển tải lên Etherscan, sau đó trình biên dịch của Etherscan biên dịch lại với cùng phiên bản compiler và đối chiếu thấy trùng khớp 100% với bytecode on-chain.
- **Ý nghĩa thẩm định rủi ro:** Nếu một dự án không công bố mã nguồn đã xác thực (chỉ có bytecode), nhà đầu tư và người làm tuân thủ **không thể biết bên trong có bẫy thanh khoản (honeypot), quyền rút ruột tiền hay không**. Không xác thực là dấu hiệu cảnh báo đỏ (red flag) nghiêm trọng.

### 2. Phân biệt Hàm Đọc (Read Contract) và Hàm Ghi (Write Contract)
- **Hàm Đọc (Read Contract):** Các hàm có từ khóa `view` hoặc `pure` (ví dụ: `name()`, `symbol()`, `totalSupply()`, `balanceOf(address)`).
  - *Đặc điểm:* Chỉ truy vấn trạng thái từ bộ lưu trữ của blockchain, không thay đổi dữ liệu sổ cái.
  - *Chi phí & Thao tác:* **Hoàn toàn miễn phí (0 gas)**, không cần kết nối ví MetaMask, không cần ký giao dịch.
- **Hàm Ghi (Write Contract):** Các hàm làm thay đổi trạng thái sổ cái (ví dụ: `transfer()`, `approve()`, `addBlackList()`, `mint()`).
  - *Đặc điểm:* Ghi dữ liệu mới vào blockchain, cập nhật số dư hoặc quyền hạn.
  - *Chi phí & Thao tác:* **Phải trả phí gas**, bắt buộc phải kết nối ví để ký giao dịch phát sóng lên mạng lưới P2P.

---

## PHẦN 3: ĐỌC HỢP ĐỒNG THẬT TRÊN ETHERSCAN & TRẢ LỜI 3 CÂU HỎI (BƯỚC 3)

Hợp đồng phân tích chính: **USDT (Tether USD)** trên Ethereum Mainnet  
- Địa chỉ: `0xdAC17F958D2ee523a2206206994597C13D831ec7`  
Hợp đồng phân tích mở rộng: **USDC (USD Coin)** trên Ethereum Mainnet  
- Địa chỉ: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (Mô hình EIP-1967 Proxy)

---

### Câu hỏi 1: Hợp đồng bạn xem có công bố mã nguồn đã xác thực không?

**Trả lời:**  
- **USDT (`0xdAC17F958D2ee523a2206206994597C13D831ec7`):**  
  **Có công bố mã nguồn đã xác thực.** Trên Etherscan, tab `Contract` hiển thị dấu tích xanh **Contract Source Code Verified**, trình biên dịch `v0.4.18+commit.9cf6e910`, tối ưu hóa Enabled. Toàn bộ mã nguồn Solidity của hợp đồng `TetherToken` hiển thị công khai.
- **USDC (`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`):**  
  **Có công bố mã nguồn đã xác thực.** Hợp đồng triển khai dạng **FiatTokenProxy** (mẫu Proxy EIP-1967). Cả mã nguồn của Proxy và mã nguồn hợp đồng thực thi logic bên dưới (`FiatTokenV2_2` tại địa chỉ implementation) đều đã được xác thực hoàn toàn trên Etherscan.

---

### Câu hỏi 2: Tổng cung của đồng đó là bao nhiêu? Đọc ra từ hàm nào?

**Trả lời:**  
- **Tên hàm đọc:** Hàm `totalSupply()` (thuộc tab **Read Contract** trên Etherscan).
- **Với USDT (`TetherToken`):**
  - Khi gọi hàm `totalSupply()` trong tab Read Contract, hàm trả về một số nguyên lớn (ví dụ: `71,324,561,024,582,314`).
  - Do USDT có thuộc tính `decimals = 6` (đọc từ hàm `decimals()`), tổng cung thực tế lưu hành bằng giá trị trả về chia cho $10^6$:
    $$\text{Tổng cung USDT} = \frac{71,324,561,024,582,314}{10^6} \approx 71,324,561,024.58\text{ USDT (Hơn 71.3 tỷ USD)}$$
- **Với USDC (`FiatTokenProxy`):**
  - Mở tab **Read as Proxy**, gọi hàm `totalSupply()`. USDC cũng có `decimals = 6`. Giá trị trả về chia cho $10^6$ biểu diễn tổng lượng USDC đang lưu hành trên mạng Ethereum Mainnet.

---

### Câu hỏi 3: Trong tab Write Contract (với USDC: Write as Proxy), có hàm nào cho phép một địa chỉ đặc biệt đóng băng tài khoản người khác không? Nếu có, tên hàm là gì?

**Trả lời:**  
**CÓ.** Cả hai đồng ổn định giá lớn nhất thế giới (USDT và USDC) đều được thiết kế sẵn các hàm có chủ đích để đóng băng tài khoản người dùng:

1. **Đối với USDT (Tether USD):**
   - Trong tab **Write Contract**, hàm đóng băng có tên là:  
     `addBlackList(address _evilUser)`
   - Hàm gỡ bỏ đóng băng:  
     `removeBlackList(address _clearedUser)`
   - Hàm hủy số dư của tài khoản bị đóng băng:  
     `destroyBlackFunds(address _blackListedUser)`
   - **Quyền hạn gọi:** Chỉ chủ sở hữu hợp đồng (`owner`) mới có quyền thực thi nhờ kiểm tra `onlyOwner`. Khi một địa chỉ bị đưa vào danh sách đen, biến `isBlackListed[_evilUser]` được gán bằng `true`. Trong các hàm `transfer` và `transferFrom`, hợp đồng kiểm tra nếu địa chỉ gửi hoặc nhận nằm trong danh sách đen thì sẽ bị `revert`, vô hiệu hóa hoàn toàn khả năng chuyển/nhận USDT.

2. **Đối với USDC (USD Coin):**
   - Trong tab **Write as Proxy**, hàm đóng băng có tên là:  
     `blacklist(address _account)`
   - Hàm gỡ bỏ đóng băng:  
     `unBlacklist(address _account)`
   - **Quyền hạn gọi:** Chỉ vai trò `blacklister` (được cấp bởi ban quản trị Center / Circle) mới có quyền gọi hàm này (`onlyBlacklister`). Địa chỉ bị `blacklist` sẽ bị chặn mọi giao dịch phát sinh.

#### Ý nghĩa nghiệp vụ & Thảo luận về tính phi tập trung thực tế:
- **Tính phi tập trung tương đối:** Nhiều người lầm tưởng tiền mã hóa là hoàn toàn phi tập trung và không ai có thể can thiệp số dư ví. Tuy nhiên, các đồng stablecoin tập trung như USDT hay USDC thực chất là **tài sản số chịu quản lý tập trung (centralized token on decentralized ledger)**. Tổ chức phát hành (Tether/Circle) giữ chìa khóa quản trị tối thượng.
- **Góc nhìn Tuân thủ & Pháp lý:** Cơ chế này là bắt buộc để Tether và Circle tuân thủ quy định pháp luật quốc tế (yêu cầu đóng băng của tòa án, Bộ Tài chính Hoa Kỳ OFAC đối với các địa chỉ liên quan đến rửa tiền, tội phạm mạng, mã độc tống tiền hoặc tấn công giao thức DeFi).

---

## PHẦN 4: NHẬT KÝ LÀM VIỆC VỚI AI (AI_JOURNAL)

### Lần 1
- **Prompt:** *"Trong hợp đồng USDC trên Etherscan, tôi vào tab Write Contract để tìm hàm đóng băng tài khoản nhưng chỉ thấy các hàm upgradeTo, changeAdmin mà không thấy hàm blacklist. Hãy giải thích tại sao."*
- **AI trả về:** AI giải thích rằng hợp đồng USDC không có hàm đóng băng tài khoản, mã nguồn của USDC là hoàn toàn phi tập trung và không ai có quyền đóng băng ví của người dùng.
- **Đánh giá:** ❌ Sai, bỏ hoàn toàn nhận định của AI.
- **Chỗ sai:**  
  1. AI không nhận diện được kiến trúc **Proxy Pattern (EIP-1967)** của USDC. Tab `Write Contract` chỉ hiển thị các hàm của hợp đồng Proxy quản trị việc nâng cấp.  
  2. Toàn bộ logic nghiệp vụ token (gồm `totalSupply`, `transfer`, `blacklist`) nằm tại hợp đồng Implementation. Để thấy hàm đóng băng, phải chọn tab **Write as Proxy**.  
  3. AI ngộ nhận về tính phi tập trung của stablecoin, phủ nhận sự tồn tại của chức năng `blacklist`.
- **Cách sửa:** Sinh viên tự tra cứu tài liệu Etherscan về Proxy Contract, chuyển sang tab `Write as Proxy` trên giao diện Etherscan tại địa chỉ `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`, tìm thấy chính xác hàm `blacklist(address _account)`.
- **Ai phát hiện:** Sinh viên phát hiện.
