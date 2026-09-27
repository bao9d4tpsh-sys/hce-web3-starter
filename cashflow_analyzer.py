# cashflow_analyzer.py - Cong cu phan tich dong tien on-chain theo SPEC.md
# Hoc phan: ECO2432 - Lab 06
# Quy tac: Chu thich trong ma viet bang tieng Viet khong dau theo AGENTS.md

import os
import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
import matplotlib.pyplot as plt

# Hang so quy doi don vi
WEI_IN_ETH = 10**18

def get_env_api_key():
    # Doc khoa API tu bien moi truong, khong ghi thang vao ma nguon
    api_key = os.environ.get("ETHERSCAN_API_KEY")
    return api_key

def fetch_wallet_balance(address, api_key, network="sepolia"):
    # Lay so du hien tai cua vi qua RPC hoac Etherscan API
    # Kiem tra ma trang thai truoc khi xu ly du lieu
    if network == "sepolia":
        base_url = "https://api-sepolia.etherscan.io/api"
    else:
        base_url = "https://api.etherscan.io/api"

    url = f"{base_url}?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                print(f"[Canh bao] HTTP code {response.status} khi goi balance.")
                return 0.0
            data = json.loads(response.read().decode())
            if data.get("status") == "1":
                # Doi wei sang ETH truoc khi hien thi hoac tinh toan
                balance_wei = int(data.get("result", 0))
                return balance_wei / WEI_IN_ETH
            else:
                return 0.0
    except Exception as e:
        print(f"[Canh bao] Khong the lay so du online: {e}")
        return 0.0

def fetch_transactions(address, api_key, days=90, network="sepolia"):
    # Truy van lich su giao dich trong khoang thoi gian quy dinh
    if network == "sepolia":
        base_url = "https://api-sepolia.etherscan.io/api"
    else:
        base_url = "https://api.etherscan.io/api"

    now_ts = int(datetime.now(timezone.utc).timestamp())
    start_ts = now_ts - (days * 86400)
    
    all_txs = []
    page = 1
    offset = 1000

    print(f"[*] Dang tai du lieu cho vi: {address} trong {days} ngay qua...")

    while True:
        url = (
            f"{base_url}?module=account&action=txlist&address={address}"
            f"&startblock=0&endblock=99999999&page={page}&offset={offset}"
            f"&sort=asc&apikey={api_key}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                # Kiem tra ma trang thai phan hoi
                if res.status != 200:
                    print(f"[Loi] HTTP status {res.status}")
                    break
                data = json.loads(res.read().decode())
        except urllib.error.HTTPError as e:
            print(f"[Loi] Yeu cau API that bai: {e.code} - {e.reason}")
            sys.exit(1)
        except Exception as e:
            print(f"[Loi ket noi]: {e}")
            break

        # Kiem tra phan hoi tu Etherscan
        status = data.get("status")
        message = data.get("message")
        result = data.get("result")

        if status == "0":
            if "No transactions found" in str(result) or "No transactions found" in str(message):
                # E1: API tra ve danh sach rong
                print("Vi khong co giao dich trong ky")
                return []
            else:
                # E2: Loi API Key hoac thong bao loi tu Etherscan
                print(f"[Loi API Etherscan] Status: {status}, Thong bao: {message}, Chi tiet: {result}")
                print("-> Vui long kiem tra lai bien moi truong ETHERSCAN_API_KEY hoac ket noi mang.")
                return []

        if not isinstance(result, list):
            break

        for tx in result:
            tx_ts = int(tx.get("timeStamp", 0))
            if tx_ts >= start_ts:
                all_txs.append(tx)

        if len(result) < offset:
            # Da lay het du lieu
            break
        
        # R9: Nghi 0.25 giay tranh bi rate limit 5 req/s
        page += 1
        time.sleep(0.25)

    return all_txs

def analyze_cashflow(address, txs, current_balance=0.0):
    # Phan tich dong tien theo cac quy tac R1 -> R8 trong SPEC.md
    target_addr = address.lower()
    
    # R6: Sap xep theo thoi gian tang dan
    txs_sorted = sorted(txs, key=lambda x: int(x.get("timeStamp", 0)))
    
    records = []
    total_inflow = 0.0
    total_outflow = 0.0

    for tx in txs_sorted:
        from_addr = tx.get("from", "").lower()
        to_addr = (tx.get("to") or "").lower() # E5: Xu ly to co the la None
        value_wei = int(tx.get("value", 0))
        value_eth = value_wei / WEI_IN_ETH # R5: Doi wei sang ETH

        gas_used = int(tx.get("gasUsed", 0))
        gas_price = int(tx.get("gasPrice", 0))
        fee_eth = (gas_used * gas_price) / WEI_IN_ETH # R5: Doi phi wei sang ETH

        is_error = tx.get("isError") == "1"
        ts = int(tx.get("timeStamp", 0))
        dt_str = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M")
        tx_hash = tx.get("hash", "")
        tx_hash_short = f"{tx_hash[:6]}...{tx_hash[-4:]}" if len(tx_hash) > 10 else tx_hash

        flow_type = "UNKNOWN"
        net_change = 0.0

        if from_addr == target_addr and to_addr == target_addr:
            # R7: Giao dich tu chuyen cho chinh minh
            flow_type = "SELF_TRANSFER"
            total_outflow += fee_eth
            net_change = -fee_eth
        elif to_addr == target_addr and not is_error:
            # R1: Dong tien vao thanh cong
            flow_type = "INFLOW"
            total_inflow += value_eth
            net_change = value_eth
        elif from_addr == target_addr:
            if not is_error:
                # R2 & R3: Dong tien ra thanh cong gom value va phi gas
                flow_type = "OUTFLOW"
                actual_deducted = value_eth + fee_eth
                total_outflow += actual_deducted
                net_change = -actual_deducted
            else:
                # R4: Giao dich that bai van bi tru phi gas
                flow_type = "FAILED_FEE"
                total_outflow += fee_eth
                net_change = -fee_eth
        else:
            continue

        records.append({
            "datetime": dt_str,
            "timestamp": ts,
            "hash": tx_hash_short,
            "type": flow_type,
            "value_eth": value_eth,
            "fee_eth": fee_eth,
            "net_change": net_change
        })

    # R8: Tinh so du goc dau ky
    net_period_change = total_inflow - total_outflow
    base_balance = current_balance - net_period_change
    if base_balance < 0:
        base_balance = 0.0 # Phong truong hop vi khong lay duoc online balance

    cumulative = base_balance
    timestamps = []
    balances = []

    for r in records:
        cumulative += r["net_change"]
        r["cumulative_balance"] = cumulative
        timestamps.append(datetime.fromtimestamp(r["timestamp"], timezone.utc))
        balances.append(cumulative)

    return {
        "records": records,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "ending_balance": cumulative,
        "timestamps": timestamps,
        "balances": balances
    }

def print_report(summary, records):
    # In bao cao dong tien dang bang
    print("\n" + "="*80)
    print(f"{'THOI GIAN (UTC)':<18} | {'HASH':<14} | {'LOAI':<12} | {'CHUYEN (ETH)':<14} | {'PHI (ETH)':<12} | {'LUY KE (ETH)'}")
    print("-"*80)
    for r in records:
        print(f"{r['datetime']:<18} | {r['hash']:<14} | {r['type']:<12} | {r['value_eth']:<14.6f} | {r['fee_eth']:<12.6f} | {r['cumulative_balance']:.6f}")
    print("="*80)
    print(f"[BA CON SO TONG HOP TAI CHINH]")
    print(f"1. Tong dong tien vao : +{summary['total_inflow']:.6f} ETH")
    print(f"2. Tong dong tien ra  : -{summary['total_outflow']:.6f} ETH (Da gom phi gas)")
    print(f"3. So du cuoi ky      :  {summary['ending_balance']:.6f} ETH")
    print("="*80 + "\n")

def plot_balance_chart(timestamps, balances, output_path="balance_chart.png"):
    # Ve bieu do duong bien dong so du luy ke theo thoi gian
    if not timestamps or not balances:
        print("[Thong bao] Khong co du lieu de ve bieu do.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, balances, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label="So du vi (ETH)")
    plt.fill_between(timestamps, balances, alpha=0.2, color='#1f77b4')
    plt.title("Bieu do bien dong so du luy ke theo thoi gian (90 ngay qua)", fontsize=13, fontweight='bold')
    plt.xlabel("Moc thoi gian", fontsize=11)
    plt.ylabel("So du (ETH)", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Luu file anh
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Thanh cong] Da xuat bieu do bien dong so du tai: {output_path}")

def generate_sample_dataset():
    # Du lieu mau kiem thu 90 ngay gom ca giao dich thanh cong, that bai, tu chuyen
    # Giup sinh vien co the chay thu nghiem ngay lap tuc
    now_ts = int(datetime.now(timezone.utc).timestamp())
    sample_addr = "0x113b614b6a21f5ec532a4cf4d71dfa8fe68be688"
    other_addr1 = "0xdeadc0dec18f9f380c7c272e366a5e0b32aa1eff"
    other_addr2 = "0x8f6eb7870334b1fd8006fd52413f01689f4e57e9"

    txs = [
        # Giao dich 1: Nhan 1.5 ETH (Inflow) cach day 80 ngay
        {
            "timeStamp": str(now_ts - 80 * 86400),
            "from": other_addr1,
            "to": sample_addr,
            "value": str(int(1.5 * WEI_IN_ETH)),
            "gasUsed": "21000",
            "gasPrice": str(int(5 * 10**9)),
            "isError": "0",
            "hash": "0xbf85d1b058d3acd41dca546a01990f5f7a86fae4c5877306051aea6ddbcff79f"
        },
        # Giao dich 2: Chuyen 0.5 ETH di (Outflow) cach day 50 ngay
        {
            "timeStamp": str(now_ts - 50 * 86400),
            "from": sample_addr,
            "to": other_addr2,
            "value": str(int(0.5 * WEI_IN_ETH)),
            "gasUsed": "21000",
            "gasPrice": str(int(10 * 10**9)),
            "isError": "0",
            "hash": "0x789c614b6a21f5ec532a4cf4d71dfa8fe68be688111122223333444455556666"
        },
        # Giao dich 3: Giao dich that bai co chu dich (Failed Outflow) cach day 25 ngay
        # Value hoan lai, phi gas van bi tru
        {
            "timeStamp": str(now_ts - 25 * 86400),
            "from": sample_addr,
            "to": other_addr1,
            "value": str(int(0.8 * WEI_IN_ETH)),
            "gasUsed": "88998",
            "gasPrice": str(int(8 * 10**9)),
            "isError": "1",
            "hash": "0xa365408fe04d15564e154e46d10b0d85395e28b2ed5e7695786d5e098ecdf8a6"
        },
        # Giao dich 4: Tu chuyen tien cho chinh minh (Self-transfer) cach day 10 ngay
        {
            "timeStamp": str(now_ts - 10 * 86400),
            "from": sample_addr,
            "to": sample_addr,
            "value": str(int(0.1 * WEI_IN_ETH)),
            "gasUsed": "21000",
            "gasPrice": str(int(6 * 10**9)),
            "isError": "0",
            "hash": "0x444455556666777788889999aaaabbbbccccddddeeeeffff0000111122223333"
        },
        # Giao dich 5: Nhan them 0.2 ETH cach day 2 ngay
        {
            "timeStamp": str(now_ts - 2 * 86400),
            "from": other_addr2,
            "to": sample_addr,
            "value": str(int(0.2 * WEI_IN_ETH)),
            "gasUsed": "21000",
            "gasPrice": str(int(4 * 10**9)),
            "isError": "0",
            "hash": "0x555566667777888899990000111122223333444455556666777788889999aaaa"
        }
    ]
    return sample_addr, txs

def main():
    print("="*60)
    print(" ECO2432 - ETH CASH FLOW ANALYZER (LAB 06)")
    print("="*60)

    # 1. Kiem tra khoa API
    api_key = get_env_api_key()
    target_address = sys.argv[1] if len(sys.argv) > 1 else None

    if not api_key or not target_address:
        print("[Thong bao] Khong tim thay ETHERSCAN_API_KEY hoac tham so dia chi vi.")
        print("[*] Khoi chay che do Kiem thu Mau (Sample Mock Test Mode) theo SPEC.md...")
        sample_addr, sample_txs = generate_sample_dataset()
        analysis = analyze_cashflow(sample_addr, sample_txs, current_balance=1.1983)
        print_report(analysis, analysis["records"])
        plot_balance_chart(analysis["timestamps"], analysis["balances"], output_path="balance_chart.png")
        # Dong thoi luu vao thu muc evidence/lab-06 theo tieu chuan
        plot_balance_chart(analysis["timestamps"], analysis["balances"], output_path="evidence/lab-06/balance_chart.png")
        print("\n[Huong dan chay that voi Etherscan]:")
        print("  set ETHERSCAN_API_KEY=YOUR_KEY (tren Windows CMD)")
        print("  $env:ETHERSCAN_API_KEY=\"YOUR_KEY\" (tren PowerShell)")
        print("  python cashflow_analyzer.py <dia_chi_vi>")
        return

    # Chay online that
    txs = fetch_transactions(target_address, api_key, days=90)
    if not txs:
        print("Vi khong co giao dich trong ky hoac gap loi.")
        return

    current_balance = fetch_wallet_balance(target_address, api_key)
    analysis = analyze_cashflow(target_address, txs, current_balance=current_balance)
    print_report(analysis, analysis["records"])
    plot_balance_chart(analysis["timestamps"], analysis["balances"], output_path="balance_chart.png")
    plot_balance_chart(analysis["timestamps"], analysis["balances"], output_path="evidence/lab-06/balance_chart.png")

if __name__ == "__main__":
    main()
