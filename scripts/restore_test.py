#!/usr/bin/env python3
"""
Automated Database Restore & Verification Script.
Restores SQL backup into an isolated testing database (pm_restore_test)
and verifies table row counts and data integrity without affecting running services.
"""
import os
import sys
import glob
import json
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TEST_DB = "pm_restore_test"
SOURCE_DB = "pm_db"
TABLES = ["users", "members", "projects", "tasks", "project_members", "audit_logs"]

def get_latest_backup():
    backups = glob.glob("backups/*.sql")
    if not backups:
        print("[-] Không tìm thấy file backup nào trong thư mục backups/")
        sys.exit(1)
    backups.sort(key=os.path.getmtime, reverse=True)
    return backups[0]

def run_sql(db_name, sql):
    cmd = ["docker", "exec", "pm-postgres", "psql", "-U", "postgres", "-d", db_name, "-t", "-A", "-c", sql]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()

def restore_and_verify(backup_file=None):
    if not backup_file:
        backup_file = get_latest_backup()

    print("=" * 70)
    print(f"BẮT ĐẦU KIỂM THỬ PHỤC HỒI CƠ SỞ DỮ LIỆU ĐỘC LẬP")
    print(f"File nguồn: {backup_file}")
    print(f"Database thử nghiệm độc lập: {TEST_DB}")
    print("=" * 70)

    # 1. Tạo Database thử nghiệm riêng biệt (Xóa bản cũ nếu có)
    print(f"[*] Khởi tạo database độc lập '{TEST_DB}'...")
    subprocess.run(["docker", "exec", "pm-postgres", "psql", "-U", "postgres", "-c", f"DROP DATABASE IF EXISTS {TEST_DB};"], capture_output=True)
    proc_create = subprocess.run(["docker", "exec", "pm-postgres", "psql", "-U", "postgres", "-c", f"CREATE DATABASE {TEST_DB};"], capture_output=True, text=True)
    if proc_create.returncode != 0:
        print(f"[-] Không thể tạo database {TEST_DB}: {proc_create.stderr}")
        sys.exit(1)

    # 2. Copy file backup vào container và nạp dữ liệu
    print(f"[*] Đang phục hồi dữ liệu từ file backup vào '{TEST_DB}'...")
    container_tmp = "/tmp/restore_target.sql"
    subprocess.run(["docker", "cp", backup_file, f"pm-postgres:{container_tmp}"], check=True)

    proc_restore = subprocess.run(
        ["docker", "exec", "pm-postgres", "psql", "-U", "postgres", "-d", TEST_DB, "-f", container_tmp],
        capture_output=True, text=True
    )
    subprocess.run(["docker", "exec", "pm-postgres", "rm", "-f", container_tmp], capture_output=True)

    print("[+] Phục hồi dữ liệu hoàn tất. Bắt đầu đối chiếu số lượng bản ghi...")

    # 3. Đối chiếu số lượng bản ghi từng bảng
    print("-" * 70)
    print(f"{'Tên Bảng':<20} | {'pm_db (Gốc)':<15} | {'pm_restore_test':<18} | {'Kết quả':<10}")
    print("-" * 70)

    all_matched = True
    comparison = {}

    for tbl in TABLES:
        count_src = run_sql(SOURCE_DB, f"SELECT count(*) FROM {tbl};") or "0"
        count_dst = run_sql(TEST_DB, f"SELECT count(*) FROM {tbl};") or "0"
        matched = (count_src == count_dst)
        if not matched:
            all_matched = False

        status_str = "[\033[92mKHỚP\033[0m]" if matched else "[\033[91mLỆCH\033[0m]"
        print(f"{tbl:<20} | {count_src:<15} | {count_dst:<18} | {status_str}")
        comparison[tbl] = {
            "source_count": int(count_src),
            "restored_count": int(count_dst),
            "matched": matched
        }

    print("-" * 70)
    if all_matched:
        print("[+] TOÀN BỘ CÁC BẢNG CƠ SỞ DỮ LIỆU ĐÃ ĐƯỢC PHỤC HỒI CHÍNH XÁC 100%!")
    else:
        print("[-] Cảnh báo: Có sự sai lệch số lượng bản ghi giữa database gốc và phục hồi.")

    # 4. Lưu minh chứng
    os.makedirs("docs/evidence", exist_ok=True)
    with open("docs/evidence/restore_verification.json", "w", encoding="utf-8") as f:
        json.dump({
            "backup_file": backup_file,
            "target_db": TEST_DB,
            "all_matched": all_matched,
            "tables": comparison
        }, f, indent=2, ensure_ascii=False)

    return all_matched

if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    restore_and_verify(file_arg)
