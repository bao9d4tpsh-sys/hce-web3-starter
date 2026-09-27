# BÁO CÁO THỰC HÀNH LAB 06: SINH MÃ BẰNG AI VÀ KIỂM TRA KẾT QUẢ
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Kho lưu trữ GitHub:** [https://github.com/bao9d4tpsh-sys/hce-web3-starter](https://github.com/bao9d4tpsh-sys/hce-web3-starter)  
**Mã nguồn chương trình:** [`cashflow_analyzer.py`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/cashflow_analyzer.py)  
**Tệp biểu đồ minh chứng:** [`evidence/lab-06/balance_chart.png`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/evidence/lab-06/balance_chart.png)  
**Nhật ký lỗi AI:** [`AI_JOURNAL.md`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/AI_JOURNAL.md)  
**Chuẩn đầu ra:** Chương trình chạy ra được biểu đồ số dư lũy kế, và sinh viên ghi nhận được ít nhất 2 lỗi do công cụ AI sinh ra.

---

## 1. Kết quả thực nghiệm chương trình

Chương trình Python [`cashflow_analyzer.py`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/cashflow_analyzer.py) được xây dựng tuân thủ 100% đặc tả [`SPEC.md`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/SPEC.md) và các quy ước nghiêm ngặt trong [`AGENTS.md`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/AGENTS.md):
- Đọc khóa API từ biến môi trường `ETHERSCAN_API_KEY`.
- Kiểm tra mã trạng thái HTTP và mã phản hồi JSON trước khi xử lý.
- Đổi Wei sang ETH trước khi hiển thị (chia $10^{18}$).
- Chú thích trong mã viết bằng tiếng Việt không dấu.

### 1.1. Bảng số liệu dòng tiền chi tiết (Console Output)
```text
================================================================================
THOI GIAN (UTC)    | HASH           | LOAI         | CHUYEN (ETH)   | PHI (ETH)    | LUY KE (ETH)
--------------------------------------------------------------------------------
2026-07-09 17:07   | 0xbf85...f79f  | INFLOW       | 1.500000       | 0.000105     | 1.500000
2026-08-08 17:07   | 0x789c...6666  | OUTFLOW      | 0.500000       | 0.000210     | 0.999790
2026-09-02 17:07   | 0xa365...f8a6  | FAILED_FEE   | 0.800000       | 0.000712     | 0.999078
2026-09-17 17:07   | 0x4444...3333  | SELF_TRANSFER| 0.100000       | 0.000126     | 0.998952
2026-09-25 17:07   | 0x5555...aaaa  | INFLOW       | 0.200000       | 0.000084     | 1.198952
================================================================================
```

### 1.2. Ba con số tài chính tổng hợp (Summary KPIs)
1. **Tổng dòng tiền vào:** `+1.700000 ETH`
2. **Tổng dòng tiền ra:** `-0.501048 ETH` *(Bao gồm tiền chuyển, phí giao dịch thành công, phí giao dịch thất bại và phí tự chuyển ví)*
3. **Số dư cuối kỳ:** `1.198952 ETH`

### 1.3. Biểu đồ biến động số dư lũy kế
Đã xuất biểu đồ dạng ảnh PNG độ phân giải cao tại:
👉 [`evidence/lab-06/balance_chart.png`](file:///c:/Users/Bao/Downloads/hce-web3-starter/hce-web3-starter/evidence/lab-06/balance_chart.png)

---

## 2. Danh mục 6 điểm kiểm tra bắt buộc (Bước 2)

| # | Hạng mục kiểm tra | Cách kiểm tra | Kết quả mã AI sinh ra ban đầu | Đánh giá & Cách sinh viên sửa | Ai phát hiện |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Đơn vị tiền** | Kiểm tra số dư hiển thị có hợp lý không | ✅ Đã chia cho $10^{18}$ để đổi từ Wei sang ETH. | Đạt yêu cầu. | AI tự nhận |
| **2** | **Khóa API** | Tìm chuỗi khóa API trong mã nguồn | ❌ AI ghi cứng: `API_KEY = "YourKeyHere"` trong mã nguồn. | **Lỗi bảo mật nghiêm trọng.** Sửa lại: dùng `os.environ.get("ETHERSCAN_API_KEY")`. | **Sinh viên** |
| **3** | **Phân trang** | Kiểm tra ví có nhiều hơn 10.000 tx | ⚠️ AI chỉ gọi 1 request với `offset=10000`, không có vòng lặp lấy trang tiếp theo. | Thiếu dữ liệu nếu ví lớn. Sửa lại: thêm vòng lặp `while True` tăng `page += 1`. | **Sinh viên** |
| **4** | **Giao dịch thất bại** | Có tính phí gas của giao dịch thất bại không | ❌ AI lọc `isError == "0"`, bỏ qua hoàn toàn giao dịch thất bại! | **Lỗi nghiệp vụ kế toán nghiêm trọng:** Giao dịch lỗi vẫn bị trừ phí gas on-chain. Sửa lại: tính phí gas vào `total_outflow`. | **Sinh viên** |
| **5** | **Xử lý lỗi** | Thử nhập API key sai hoặc endpoint lỗi | ❌ Chương trình crash đột ngột với lỗi `KeyError` do không kiểm tra `status == "1"`. | **Lỗi runtime.** Sửa lại: kiểm tra HTTP status code và mã phản hồi JSON trước khi truy xuất dữ liệu. | **Sinh viên** |
| **6** | **Phiên bản API** | Đối chiếu tài liệu Etherscan hiện hành | ⚠️ AI dùng endpoint v1 cũ và thiếu độ trễ phân trang, dễ bị lỗi HTTP 429 Rate Limit. | Sửa lại: cập nhật endpoint chuẩn `api-sepolia.etherscan.io`, thêm `time.sleep(0.25)` giữa các trang truy vấn. | **Sinh viên** |

---

## 3. Cách chạy chương trình

### Cách 1: Chạy chế độ kiểm thử mẫu (Không cần API Key)
Chương trình được thiết kế sẵn bộ dữ liệu mẫu 90 ngày chuẩn mực mô phỏng đầy đủ các tình huống:
```bash
python cashflow_analyzer.py
```
Chương trình sẽ tự động phân tích 5 giao dịch mẫu, in bảng báo cáo và xuất biểu đồ ra `balance_chart.png` và `evidence/lab-06/balance_chart.png`.

### Cách 2: Chạy trực tiếp với dữ liệu ví trên mạng Etherscan
Thiết lập biến môi trường khóa API Etherscan và truyền địa chỉ ví:
- **Trên Windows PowerShell:**
  ```powershell
  $env:ETHERSCAN_API_KEY="YOUR_API_KEY"
  python cashflow_analyzer.py 0x113b614b6a21f5ec532a4cf4d71dfa8fe68be688
  ```
- **Trên Windows Command Prompt (CMD):**
  ```cmd
  set ETHERSCAN_API_KEY=YOUR_API_KEY
  python cashflow_analyzer.py 0x113b614b6a21f5ec532a4cf4d71dfa8fe68be688
  ```
