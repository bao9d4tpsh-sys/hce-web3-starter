# BÁO CÁO THỰC HÀNH LAB 07: TRIỂN KHAI HỢP ĐỒNG THÔNG MINH ĐẦU TIÊN
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Kho lưu trữ GitHub:** [https://github.com/bao9d4tpsh-sys/hce-web3-starter](https://github.com/bao9d4tpsh-sys/hce-web3-starter)  
**Hợp đồng thực hành:** [`contracts/training/TimeLockVault.sol`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/blob/main/contracts/training/TimeLockVault.sol)  
**Công cụ triển khai:** Remix IDE ([https://remix.ethereum.org](https://remix.ethereum.org))  
**Mạng triển khai:** Sepolia Testnet  
**Mục tiêu:** Biên dịch, triển khai và tương tác với hợp đồng `TimeLockVault` thông qua MetaMask; đọc ABI và ghi lại địa chỉ hợp đồng trên Sepolia.

---

## 1. Phân tích mã nguồn trước khi triển khai (Bước 1)

### 1.1. Tổng quan kiến trúc hợp đồng `TimeLockVault`

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimeLockVault {
    address public immutable owner;       // Dòng 5: Chủ sở hữu, gán cố định khi tạo
    uint256 public immutable unlockTime;  // Dòng 6: Mốc thời gian mở khóa, không thể thay đổi

    event Deposited(address indexed from, uint256 amount);  // Sự kiện nạp tiền
    event Withdrawn(address indexed to, uint256 amount);    // Sự kiện rút tiền

    error NotOwner();
    error StillLocked(uint256 unlockAt, uint256 currentTime);
    error NothingToWithdraw();
    error ZeroAmount();
    error TransferFailed();

    constructor(uint256 lockDurationSeconds) { ... }
    function deposit() external payable { ... }
    function withdraw() external { ... }
}
```

### 1.2. Bảng phân tích từng hàm theo quy ước `AGENTS.md`

| Hàm | Loại | Người được gọi | Mô tả nghiệp vụ | Kiểm tra rủi ro |
| :--- | :---: | :--- | :--- | :--- |
| `constructor(uint256 lockDurationSeconds)` | Ghi (1 lần) | Người triển khai | Gán `owner = msg.sender`; tính `unlockTime = block.timestamp + lockDurationSeconds`. Sau khi triển khai không thể thay đổi do khai báo `immutable`. | ✅ Không rủi ro — Owner gán cố định 1 lần duy nhất khi deploy. |
| `deposit()` | Ghi / Payable | **Bất kỳ ai** | Nhận ETH gửi vào két. Kiểm tra `msg.value > 0` (revert `ZeroAmount` nếu gửi 0 ETH). Phát sự kiện `Deposited`. | ✅ Cho phép mọi người nạp — Thiết kế đúng cho két tiết kiệm nhóm. |
| `withdraw()` | Ghi | **Chỉ `owner`** | Kiểm tra 3 điều kiện theo thứ tự Checks-Effects-Interactions: (1) Phải là `owner`, (2) Đã qua `unlockTime`, (3) Số dư > 0. Chuyển ETH bằng `call{value}` và kiểm tra kết quả. | ✅ Tuân thủ CEI pattern, dùng `call` thay `transfer`, error tùy biến — **Đạt chuẩn AGENTS.md**. |

### 1.3. Đánh giá tuân thủ quy ước `AGENTS.md`

| Quy tắc `AGENTS.md` | Trạng thái |
| :--- | :---: |
| Mọi hàm thay đổi trạng thái phải phát `event` | ✅ Đạt — `deposit()` phát `Deposited`, `withdraw()` phát `Withdrawn` |
| Mọi hàm chủ sở hữu phải kiểm tra quyền rõ ràng | ✅ Đạt — Dòng 28: `if (msg.sender != owner) revert NotOwner()` |
| Áp dụng Checks - Effects - Interactions | ✅ Đạt — Kiểm tra đủ điều kiện trước, emit sau, `call` cuối |
| Chuyển ETH bằng `call{value: ...}("")` và kiểm tra kết quả | ✅ Đạt — Dòng 33–34: `(bool ok, ) = payable(owner).call{value: amount}(""); if (!ok) revert TransferFailed()` |
| Ưu tiên `error` tùy biến thay chuỗi lỗi dài | ✅ Đạt — 5 custom error được định nghĩa tại dòng 11–15 |
| Không dùng `tx.origin` để xác thực | ✅ Đạt — Kiểm tra `msg.sender` |

---

## 2. Hướng dẫn triển khai trên Remix IDE (Bước 2)

### 2.1. Các bước thực hiện

**Bước 1: Chuẩn bị Remix IDE**
1. Mở trình duyệt, truy cập [https://remix.ethereum.org](https://remix.ethereum.org).
2. Trong ngăn kéo bên trái, tạo tệp mới trong thư mục `contracts/` đặt tên là `TimeLockVault.sol`.
3. Sao chép toàn bộ mã nguồn từ [`contracts/training/TimeLockVault.sol`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/blob/main/contracts/training/TimeLockVault.sol) và dán vào.

**Bước 2: Biên dịch hợp đồng**
1. Chọn tab **Solidity Compiler** (biểu tượng chữ S góc trái).
2. Chọn phiên bản compiler `0.8.20` trở lên (phù hợp `pragma ^0.8.20`).
3. Nhấn **Compile TimeLockVault.sol**.  
4. Kết quả mong đợi: Hiển thị dấu tích xanh ✅, không có lỗi hay cảnh báo quan trọng.

**Bước 3: Triển khai lên Sepolia Testnet**
1. Chọn tab **Deploy & Run Transactions** (biểu tượng mũi tên).
2. Trong mục **Environment**, chọn **Injected Provider - MetaMask**.
3. MetaMask sẽ bật lên — xác nhận kết nối ví và đảm bảo đang ở mạng **Sepolia**.
4. Trong mục **Contract**, đảm bảo đang chọn `TimeLockVault`.
5. Điền tham số constructor: `lockDurationSeconds` = **`120`** (2 phút, phù hợp kiểm tra nhanh trong lab).
6. Nhấn **Deploy**, MetaMask bật lên — xem xét phí gas và nhấn **Confirm**.
7. Sau khi giao dịch xác nhận, địa chỉ hợp đồng xuất hiện trong phần **Deployed Contracts**.

---

## 3. Biên bản tương tác hợp đồng (Bước 3)

> **Lưu ý:** Mục này cần điền bằng dữ liệu thực tế từ quá trình thực hành trên Remix + MetaMask.  
> Các giá trị đánh dấu `[...]` là phần cần sinh viên điền vào sau khi thực hiện.

### 3.1. Thông tin triển khai

| Thông tin | Giá trị |
| :--- | :--- |
| **Địa chỉ hợp đồng trên Sepolia** | `[Dán địa chỉ hợp đồng từ Remix vào đây]` |
| **Mã băm giao dịch Deploy (TxHash)** | `[Dán TxHash từ MetaMask hoặc Remix console]` |
| **Tham số constructor** | `lockDurationSeconds = 120` |
| **Đường dẫn Etherscan** | `https://sepolia.etherscan.io/address/[CONTRACT_ADDRESS]` |
| **Thời điểm deploy (UTC)** | `[Điền từ Etherscan]` |

### 3.2. Kiểm thử hàm `deposit()` — Nạp tiền vào két

| Tham số | Giá trị |
| :--- | :--- |
| **Số ETH nạp vào** | `0.01 ETH` (`10000000000000000 Wei`) |
| **Tài khoản gửi** | `[Địa chỉ ví MetaMask]` |
| **TxHash giao dịch nạp tiền** | `[Dán TxHash từ Remix console]` |
| **Số dư hợp đồng sau nạp** | `0.01 ETH` |
| **Trạng thái** | Thành công / Có phát sự kiện `Deposited` |

### 3.3. Kiểm thử hàm `withdraw()` — Thử rút tiền khi còn khoá

| Tham số | Giá trị |
| :--- | :--- |
| **Thời điểm thực hiện** | Trong vòng 2 phút đầu sau deploy (còn khoá) |
| **Kết quả mong đợi** | Giao dịch `revert` với lỗi `StillLocked(unlockAt, currentTime)` |
| **Kết quả thực tế** | `[Điền kết quả quan sát từ Remix console]` |
| **TxHash (nếu có)** | Không có (MetaMask/Remix chặn trước khi broadcast) |

### 3.4. Kiểm thử hàm `withdraw()` — Rút tiền sau khi mở khoá

| Tham số | Giá trị |
| :--- | :--- |
| **Thời điểm thực hiện** | Sau 2 phút (đã qua `unlockTime`) |
| **Kết quả mong đợi** | Thành công — ETH chuyển về ví `owner`, phát sự kiện `Withdrawn` |
| **TxHash giao dịch rút tiền** | `[Dán TxHash từ Remix console]` |
| **Số dư hợp đồng sau rút** | `0 ETH` |

### 3.5. Kiểm thử tình huống gian lận — Tài khoản khác thử rút tiền

| Tham số | Giá trị |
| :--- | :--- |
| **Tài khoản thực hiện** | Tài khoản khác (không phải `owner`) |
| **Kết quả mong đợi** | Giao dịch `revert` với lỗi `NotOwner()` |
| **Kết quả thực tế** | `[Điền kết quả quan sát từ Remix console]` |
| **Bài học** | Custom error tiết kiệm gas hơn `require("Not owner")` và thể hiện rõ ràng hơn khi đọc nhật ký sự kiện. |

---

## 4. Đọc ABI và phân tích cấu trúc

ABI (Application Binary Interface) là "bản hợp đồng giao tiếp" giữa ứng dụng bên ngoài và hợp đồng thông minh. Sau khi biên dịch thành công trong Remix, ABI có thể được sao chép từ **Solidity Compiler → ABI**.

ABI của `TimeLockVault` bao gồm:
- **2 trường trạng thái công khai có getter tự động:** `owner()` và `unlockTime()` (kiểu `view`).
- **2 hàm giao dịch:** `deposit()` (payable) và `withdraw()` (non-payable).
- **2 sự kiện:** `Deposited(address indexed from, uint256 amount)` và `Withdrawn(address indexed to, uint256 amount)`.
- **5 lỗi tùy biến:** `NotOwner`, `StillLocked`, `NothingToWithdraw`, `ZeroAmount`, `TransferFailed`.

---

## 5. Ba trường hợp kiểm thử (theo quy ước `AGENTS.md`)

| # | Tên ca kiểm thử | Điều kiện đầu | Thao tác | Kết quả mong đợi | Bằng chứng |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **TC-1** | Nạp tiền hợp lệ | Hợp đồng vừa deploy, số dư = 0 | Gọi `deposit()` với `value = 0.01 ETH` từ bất kỳ tài khoản | Thành công, số dư hợp đồng tăng lên `0.01 ETH`, sự kiện `Deposited` xuất hiện trong Remix console | TxHash giao dịch nạp |
| **TC-2** | Rút tiền khi còn khoá (Luồng sai — kiểm soát nghiệp vụ) | Hợp đồng có số dư, thời gian hiện tại < `unlockTime` | Gọi `withdraw()` với tài khoản `owner` | Giao dịch bị từ chối với lỗi `StillLocked(unlockAt, currentTime)` | Thông báo lỗi trong Remix console |
| **TC-3** | Tài khoản lạ thử rút tiền (Tình huống gian lận) | Hợp đồng có số dư, thời gian đã qua `unlockTime` | Gọi `withdraw()` từ tài khoản **không phải** `owner` | Giao dịch bị từ chối ngay lập tức với lỗi `NotOwner()` | Thông báo lỗi trong Remix console |

---

## 6. Nhật ký làm việc với AI (AI_JOURNAL — Lab 07)

*(Xem chi tiết tại [`AI_JOURNAL.md`](AI_JOURNAL.md))*

### Điểm học được trong Lab 07:
1. **`immutable` vs `constant`:** Biến `immutable` được gán giá trị **một lần duy nhất trong constructor**, sau đó không thể thay đổi. Trong `TimeLockVault`, `owner` và `unlockTime` được khai báo `immutable` để tiết kiệm gas (lưu trong bytecode, không tốn slot storage) đồng thời đảm bảo không ai có thể thay đổi chủ sở hữu hay thời gian khóa sau khi triển khai.
2. **Custom Error vs Require String:** Custom error (`error NotOwner()`) tiết kiệm gas hơn `require("Not owner")` vì không lưu chuỗi ký tự vào calldata. Đây là lý do `AGENTS.md` yêu cầu ưu tiên custom error.
3. **`call` vs `transfer`:** Hàm `transfer` có giới hạn 2300 gas cứng, có thể gây lỗi nếu địa chỉ nhận là hợp đồng thông minh. Hàm `call{value: amount}("")` linh hoạt hơn, nhưng bắt buộc phải kiểm tra giá trị trả về `ok` để phát hiện thất bại.
