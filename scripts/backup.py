#!/usr/bin/env python3
"""
Automated PostgreSQL Database Backup Script.
Uses pg_dump from pm-postgres container and stores SQL dumps in backups/ directory.
"""
import os
import sys
import subprocess
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_backup():
    os.makedirs("backups", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join("backups", f"pm_db_backup_{timestamp}.sql")

    print(f"[*] Đang thực hiện sao lưu CSDL PostgreSQL (pm_db)...")
    cmd = [
        "docker", "exec", "pm-postgres",
        "pg_dump", "-U", "postgres", "--clean", "--if-exists", "pm_db"
    ]

    try:
        with open(backup_file, "w", encoding="utf-8") as f:
            proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

        if proc.returncode != 0:
            print(f"[-] Lỗi pg_dump: {proc.stderr}")
            if os.path.exists(backup_file):
                os.remove(backup_file)
            sys.exit(1)

        size_bytes = os.path.getsize(backup_file)
        size_kb = size_bytes / 1024
        print(f"[+] Sao lưu thành công: {backup_file} ({size_kb:.2f} KB)")

        # Ghi log kết quả
        os.makedirs("docs/evidence", exist_ok=True)
        with open("docs/evidence/backup_info.json", "w", encoding="utf-8") as info_f:
            import json
            json.dump({
                "timestamp": timestamp,
                "backup_file": backup_file,
                "size_bytes": size_bytes,
                "status": "SUCCESS"
            }, info_f, indent=2)

        return backup_file
    except Exception as e:
        print(f"[-] Ngoại lệ khi sao lưu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_backup()
