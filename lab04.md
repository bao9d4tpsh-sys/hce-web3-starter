# BÁO CÁO THỰC HÀNH LAB 04: NHẬN DIỆN HỢP ĐỒNG CÓ RỦI RO
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Kho lưu trữ GitHub:** [https://github.com/bao9d4tpsh-sys/hce-web3-starter](https://github.com/bao9d4tpsh-sys/hce-web3-starter)  
**Tệp trên GitHub:** [`lab04.md`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/blob/main/lab04.md)  
**Tệp mã nguồn thẩm định:** [`contracts/lab04/ClubTokens.sol`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/blob/main/contracts/lab04/ClubTokens.sol)  
**Đường dẫn Commit trên GitHub:** [Commit 30065eb](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/30065eb)  
**Mục tiêu:** Rèn luyện kỹ năng của Chuyên viên thẩm định rủi ro tài sản số (Smart Contract Risk Auditor), nhận diện các điều khoản bất lợi/lừa đảo trong mã nguồn và trích dẫn số dòng cụ thể làm bằng chứng.

---

## 1. Bảng kết luận thẩm định rủi ro (Bước 3)

| Hợp đồng | Kết luận | Tên hàm | Số dòng | Rủi ro cho người nắm giữ token |
| :---: | :---: | :--- | :---: | :--- |
| **ClubTokenA** | **An toàn**<br>*(Không có quyền đặc biệt)* | Không có | `7 – 11` | **Không có rủi ro về mặt can thiệp quyền lực hay lạm phát.** Hợp đồng không kế thừa `Ownable`, tổng cung cố định 1.000.000 CTA được đúc 1 lần duy nhất tại hàm khởi tạo. Người nắm giữ chỉ chịu rủi ro thị trường nếu người triển khai ban đầu nắm giữ 100% nguồn cung rồi bán xả ra ngoài. |
| **ClubTokenB** | **Rủi ro cao**<br>*(Lạm phát vô hạn / Infinite Mint)* | `mint(address to, uint256 amount)` | `18 – 20` | **Bị pha loãng giá trị về 0 (Rug Pull / Lạm phát vô hạn).** Chủ sở hữu (`onlyOwner`) có quyền tự ý đúc thêm token không giới hạn số lượng và không có trần tổng cung (`maxSupply`). Chủ dự án có thể đúc hàng triệu token cho ví riêng rồi bán tháo (dump) ra sàn DEX rút cạn thanh khoản bể tiền của nhà đầu tư. |
| **ClubTokenC** | **Rủi ro cực cao**<br>*(Bẫy thanh khoản / Honeypot)* | 1. `setRestricted(address user, bool status)`<br>2. `_update(address from, address to, uint256 value)` | `30 – 32`<br><br>`34 – 37` | **Bị đóng băng tài sản vĩnh viễn, không thể bán token (Mất 100% thanh khoản).** Chủ sở hữu có quyền đơn phương gán bất kỳ ví người dùng nào vào danh sách `restricted = true`. Đặc biệt tại dòng 35, hàm `_update` chỉ chặn chiều gửi `!restricted[from]`, đồng nghĩa người dùng **vẫn nạp/mua token vào được nhưng bị chặn hoàn toàn chiều bán/chuyển đi** (Mô hình bẫy Honeypot điển hình). |

---

## 2. Chi tiết phân tích mã nguồn từng hợp đồng

### 2.1. ClubTokenA (`ClubTokens.sol: L7-L11`)
```solidity
7: contract ClubTokenA is ERC20 {
8:     constructor() ERC20("Club Token A", "CTA") {
9:         _mint(msg.sender, 1_000_000 * 10 ** decimals());
10:     }
11: }
```
- **Phân tích quyền lực:** Hợp đồng chỉ kế thừa duy nhất `ERC20`, hoàn toàn không import hay kế thừa `Ownable`. Không có địa chỉ `admin` hay `owner`.
- **Cơ chế cung ứng:** Tổng cung 1.000.000 CTA được phát hành trọn vẹn trong `constructor` cho người triển khai (`msg.sender`). Không có hàm `mint` hay `burn` bổ sung.
- **Tính bất biến:** Không có hàm nào có thể thay đổi trạng thái quản trị hay can thiệp số dư ví sau khi triển khai. Đây là thiết kế chuẩn mực cho một token phi tập trung hoàn toàn.

---

### 2.2. ClubTokenB (`ClubTokens.sol: L13-L21`)
```solidity
13: contract ClubTokenB is ERC20, Ownable {
14:     constructor() ERC20("Club Token B", "CTB") Ownable(msg.sender) {
15:         _mint(msg.sender, 1_000_000 * 10 ** decimals());
16:     }
17: 
18:     function mint(address to, uint256 amount) external onlyOwner {
19:         _mint(to, amount);
20:     }
21: }
```
- **Vị trí lỗi rủi ro:** Dòng 18 – 20, hàm `mint(address to, uint256 amount) external onlyOwner`.
- **Lỗ hổng nghiệp vụ:** Hàm có modifier `onlyOwner` nhưng hoàn toàn **thiếu ràng buộc giới hạn trần tổng cung** (không có `cap` hoặc `maxSupply`).
- **Kịch bản tấn công / Thiệt hại:** Nếu chủ sở hữu ví giữ private key bị lộ hoặc nảy sinh lòng tham, họ có thể gọi `mint(my_wallet, 100_000_000_000 * 10**18)` và lập tức swap sang ETH trên Uniswap, làm giá token CTB sụp đổ về 0.

---

### 2.3. ClubTokenC (`ClubTokens.sol: L23-L38`)
```solidity
23: contract ClubTokenC is ERC20, Ownable {
24:     mapping(address => bool) public restricted;
...
30:     function setRestricted(address user, bool status) external onlyOwner {
31:         restricted[user] = status;
32:     }
33: 
34:     function _update(address from, address to, uint256 value) internal override {
35:         require(!restricted[from], "Dia chi bi han che");
36:         super._update(from, to, value);
37:     }
38: }
```
- **Vị trí lỗi rủi ro:** 
  - Dòng 30 – 32: Hàm `setRestricted` cho phép `owner` tùy tiện đổi trạng thái hạn chế của bất kỳ ai mà không cần sự đồng thuận.
  - Dòng 34 – 37: Hàm `_update` ghi đè chuẩn OpenZeppelin v5, kiểm tra điều kiện `require(!restricted[from], "Dia chi bi han che")`.
- **Bản chất bẫy Honeypot:**
  - Logic kiểm tra chỉ áp dụng với `from`, nghĩa là `to` không bị kiểm tra. Nạn nhân nhìn thấy lệnh mua token của mình trên DEX thành công bình thường.
  - Tuy nhiên khi nạn nhân muốn bán lại token trên sàn DEX (lúc này địa chỉ nạn nhân đóng vai trò là `from`), giao dịch sẽ lập tức bị từ chối với lỗi `Dia chi bi han che`. Toàn bộ số vốn mua token bị giam giữ vĩnh viễn trong hợp đồng.

---

## 3. Báo cáo so sánh: Đọc thủ công vs. Hỏi AI

| Tiêu chí | Đọc thủ công (Sinh viên thực hiện trong 15 phút đầu) | Công cụ AI phân tích (Sau khi cung cấp prompt chuẩn) |
| :--- | :--- | :--- |
| **ClubTokenA** | - Nhận thấy không có hàm `mint` hay `owner`.<br>- Kết luận token an toàn, không có cửa sau. | - Xác nhận mã an toàn, tuân thủ chuẩn ERC-20.<br>- Bổ sung thêm nhận định: Rủi ro duy nhất nằm ở việc phân phối token ban đầu (Initial Token Allocation) tập trung 100% tại `msg.sender` (dòng 9). |
| **ClubTokenB** | - Phát hiện ngay hàm `mint` ở dòng 18 có `onlyOwner`.<br>- Xác định nguy cơ lạm phát vô hạn. | - Chỉ rõ dòng 18–20.<br>- Phân tích sâu: Hợp đồng thiếu cơ chế `Cap` hoặc `Timelock` bảo vệ cộng đồng khỏi hành vi mint trộm. |
| **ClubTokenC** | - Phát hiện hàm `setRestricted` (dòng 30-32).<br>- Nhìn ra hàm `_update` có dòng require hạn chế (dòng 35). | - Phân tích chính xác cấu trúc **Honeypot**: Chỉ ra sự bất đối xứng giữa chiều nhận (`to`) và chiều gửi (`from`), giúp làm sáng tỏ thủ đoạn lừa đảo tinh vi. |

### Đánh giá lỗi sai và ảo giác của AI (AI Hallucination):
1. **Lỗi ngộ nhận về ClubTokenA:** Khi hỏi AI chung chung không có câu cấm, AI thường cho rằng: *"ClubTokenA có rủi ro nghiêm trọng vì thiếu Ownable, khiến ban quản trị không thể can thiệp khi có sự cố"*. Đây là tư duy sai lầm từ quản trị tập trung. Đối với tài sản mã hóa phi tập trung, việc không có `Ownable` là bảo chứng an toàn cao nhất chống lại sự can thiệp của con người.
2. **Lỗi bịa đặt tính năng (nếu không có câu cấm):** AI có xu hướng bịa thêm các hàm phổ biến như `pause()`, `freeze()`, hoặc `burn()` dù trong mã nguồn 40 dòng hoàn toàn không có các hàm này. Việc sử dụng câu lệnh chuẩn trong `prompt_templates.md` (*"Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy"*) đã triệt tiêu được ảo giác này.

---

## 4. Bài học nghề nghiệp cho Chuyên viên Thẩm định rủi ro (Risk Auditor)

1. **Số dòng là bằng chứng pháp lý:** Trong thẩm định bảo mật và tuân thủ, kết luận rủi ro bắt buộc phải đi kèm dẫn chứng số dòng mã nguồn cụ thể. Không thể chấp nhận báo cáo chung chung.
2. **Quy tắc Kiểm tra Blacklist/Honeypot:** Khi thẩm định bất kỳ token ERC-20 nào trước khi niêm yết hoặc tích hợp vào hệ thống thanh toán:
   - Luôn kiểm tra hàm `_update` (OpenZeppelin v5) hoặc `_beforeTokenTransfer` (v4).
   - Kiểm tra xem điều kiện chuyển tiền có bị phụ thuộc vào biến mapping nội bộ (như `restricted`, `blacklisted`, `isFeeExempt`) chịu sự kiểm soát của một địa chỉ đơn lẻ (`onlyOwner`) hay không.
3. **Quy tắc Kiểm tra Quyền Mint:** Một token có hàm `mint` mở rộng sau khi deploy bắt buộc phải có `maxSupply` cố định trong code hoặc khóa thời gian (`TimelockController`) nhiều ngày để cộng đồng kịp phản ứng khi có lệnh mint mới.
