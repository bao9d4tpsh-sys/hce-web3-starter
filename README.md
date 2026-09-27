# ECO2432 Web3 Starter — Sinh viên: Bao (`bao9d4tpsh-sys`)

**Kho lưu trữ GitHub cá nhân:** [https://github.com/bao9d4tpsh-sys/hce-web3-starter](https://github.com/bao9d4tpsh-sys/hce-web3-starter)

---

## 📌 Bảng tiến độ thực hành (Lab 01 – Lab 07)

| Bài Lab | Tên bài thực hành | Sản phẩm nộp trên GitHub | Trạng thái | Mã Commit |
| :---: | :--- | :--- | :---: | :--- |
| **Lab 01** | Chuẩn bị môi trường làm việc | [`lab01.md`](lab01.md) | ✅ Hoàn thành | [`1ddd501`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/1ddd501b98bb83f0793d9c016ec5294bc5b3a2f1) |
| **Lab 02** | Ví và giao dịch đầu tiên | [`lab02.md`](lab02.md) | ✅ Hoàn thành | [`34d31c6`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/34d31c6) |
| **Lab 03** | Đọc giao dịch & hợp đồng Etherscan | [`forensics.md`](forensics.md) / [`lab03.md`](lab03.md) | ✅ Hoàn thành | [`44c9904`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/44c9904) |
| **Lab 04** | Nhận diện hợp đồng có rủi ro | [`lab04.md`](lab04.md) & [`AI_JOURNAL.md`](AI_JOURNAL.md) | ✅ Hoàn thành | [`30065eb`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/30065eb) |
| **Lab 05** | Viết đặc tả cho công cụ phân tích dòng tiền | [`SPEC.md`](SPEC.md) & [`lab05.md`](lab05.md) | ✅ Hoàn thành | [`293c843`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/293c843) |
| **Lab 06** | Sinh mã bằng AI & kiểm tra kết quả | [`cashflow_analyzer.py`](cashflow_analyzer.py) & [`lab06.md`](lab06.md) | ✅ Hoàn thành | [`4512baa`](https://github.com/bao9d4tpsh-sys/hce-web3-starter/commit/4512baa) |
| **Lab 07** | Triển khai hợp đồng đầu tiên | [`lab07.md`](lab07.md) & [`AI_JOURNAL.md`](AI_JOURNAL.md) | ✅ Hoàn thành | Đang cập nhật |

---

Sổ tay ghi "Fork kho `hce-web3-starter`". Học kỳ này kho được phát dạng tệp nén, nên làm như sau:

1. Giải nén thư mục này vào máy, mở bằng Antigravity.
2. Đọc `AGENTS.md` trước khi yêu cầu công cụ AI sinh mã.
3. Sao chép `SPEC.md` và `AI_JOURNAL.md` cho từng bài.
4. Chỉ dùng ví thử nghiệm và mạng Sepolia; không dùng khóa ví có tiền thật.

Đưa lên GitHub (làm khi đã có tài khoản; cần trước khi nộp Lab 1):

```bash
git init -b main
git add .
git commit -m "chore: thiet lap moi truong lam viec"
git remote add origin https://github.com/<tai-khoan>/<ten-repo>.git   # repo tạo TRỐNG trên GitHub
git push -u origin main
```

Lab 8 (repo nhóm): một thành viên tạo repo trống mới, đưa nội dung thư mục này lên theo đúng các
lệnh trên, rồi mời các thành viên khác làm collaborator.

## Cấu trúc

- `contracts/training/`: hợp đồng mẫu dùng ở Lab 9, 10, 11 và 13
  (`TimeLockVault`, `VaultBuggy`, `ClassPoint`, `VulnerableBank`).
- `contracts/lab04/ClubTokens.sol`: ba token dùng cho Lab 4.
- `web/index.html`: giao diện mẫu dùng ở Lab 15.
- `prompt_templates.md`: mẫu câu lệnh có yêu cầu và tiêu chí kiểm chứng rõ ràng.

Các hợp đồng có chữ `Buggy`, `Vulnerable` hoặc cảnh báo trong mã đều chứa lỗi có chủ đích.

## Chạy hợp đồng

- Cách chính: mở Remix IDE (`https://remix.ethereum.org`), tạo tệp, dán mã. Remix tự tải thư viện
  `@openzeppelin/...`, không cần cài gì.
- Nếu Antigravity gạch đỏ dòng `import "@openzeppelin/..."`: đó là do máy chưa có thư viện, mã
  không sai. Muốn hết gạch đỏ thì cài Node.js rồi chạy `npm install` trong thư mục này (không bắt buộc).
