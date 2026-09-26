# ECO2432 Web3 Starter

Kho khởi đầu dùng xuyên suốt 15 bài thực hành.

## Bắt đầu (thay cho bước "Fork kho" trong sổ tay)

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
