# LAB 03: ĐỌC GIAO DỊCH VÀ HỢP ĐỒNG TRÊN ETHERSCAN

> **Lưu ý:** Theo đúng quy định của đề bài Sổ tay thực hành ECO2432 (Trang 11):  
> **Sản phẩm nộp của Lab 3 là tệp:** [`forensics.md`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/forensics.md).

Vui lòng xem toàn bộ nội dung chi tiết báo cáo tại tệp:  
👉 **[forensics.md](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/forensics.md)**

---

### Tóm tắt nội dung báo cáo trong `forensics.md`:
1. **Bước 1 - Mổ xẻ giao dịch on-chain:** Bảng chi tiết 10 trường dữ liệu (`Status`, `Block`, `Timestamp`, `From/To`, `Value`, `Transaction Fee`, `Gas Price`, `Gas Limit`, `Gas Used`, `Nonce`) từ giao dịch thực nghiệm Sepolia của Lab 2, gắn với góc nhìn nghiệp vụ Kế toán tài sản số và Tuân thủ AML.
2. **Bước 2 - Phân biệt bản chất kỹ thuật:**
   - Bytecode (mã máy EVM) vs. Verified Source Code (mã nguồn đã xác thực).
   - Hàm Đọc (`view`/`pure`, 0 gas, không cần ký ví) vs. Hàm Ghi (thay đổi trạng thái, mất phí gas, cần ví ký giao dịch).
3. **Bước 3 - Trả lời 3 câu hỏi hợp đồng thực tế (USDT & USDC):**
   - **Câu 1:** Xác minh mã nguồn công khai (Verified Source Code).
   - **Câu 2:** Hàm đọc tổng cung `totalSupply()` và quy tắc chia $10^{\text{decimals}}$ ($10^6$).
   - **Câu 3:** Khám phá hàm đóng băng tài khoản (`addBlackList` của USDT và `blacklist` trong tab *Write as Proxy* của USDC), phân tích quyền hạn (`owner`/`blacklister`) và thảo luận chuyên sâu về tính phi tập trung thực tế.
4. **Nhật ký AI (`AI_JOURNAL`):** Ghi lại lỗi sai của AI khi không nhận biết cơ chế Proxy Contract EIP-1967.
