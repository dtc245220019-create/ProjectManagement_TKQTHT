#!/usr/bin/env python3
"""
Automated Screenshot Capture Tool for Evidence Collection.
Uses headless Microsoft Edge with Selenium to capture crisp, high-resolution screenshots
of the running system: Website, Projects, Tasks, Members, pgAdmin, Prometheus, Grafana, and Loki queries.
"""
import os
import sys
import time
import requests
import urllib3

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

EVIDENCE_DIR = "docs/evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(30)
    return driver

def capture_all():
    print("=" * 70)
    print("BẮT ĐẦU CHỤP ẢNH MINH CHỨNG THỰC TẾ TỪ HỆ THỐNG ĐANG CHẠY")
    print("=" * 70)

    driver = get_driver()
    try:
        # 1. Đăng nhập Website
        print("[*] Đang truy cập trang đăng nhập https://localhost:8443/login...")
        driver.get("https://localhost:8443/login")
        time.sleep(2)

        # Điền form đăng nhập
        user_input = driver.find_element(By.ID, "username")
        pass_input = driver.find_element(By.ID, "password")
        user_input.send_keys("admin")
        pass_input.send_keys("Admin@ProjectMgmt2026!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # 1. Dashboard
        print("[+] Chụp ảnh 01: Dashboard tổng quan...")
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "01_website_home_dashboard.png"))

        # 2. Danh sách dự án
        print("[+] Chụp ảnh 02: Danh sách dự án...")
        driver.get("https://localhost:8443/projects")
        time.sleep(2)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "02_website_projects_list.png"))

        # 3. Chi tiết dự án PRJ-001
        print("[+] Chụp ảnh 03: Chi tiết dự án PRJ-001...")
        driver.get("https://localhost:8443/projects/1")
        time.sleep(2)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "03_website_project_detail.png"))

        # 4. Quản lý công việc (Tasks)
        print("[+] Chụp ảnh 04: Quản lý công việc (Tasks)...")
        driver.get("https://localhost:8443/tasks")
        time.sleep(2)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "04_website_tasks_management.png"))

        # 5. Quản lý thành viên (Members)
        print("[+] Chụp ảnh 05: Quản lý thành viên (Members)...")
        driver.get("https://localhost:8443/members")
        time.sleep(2)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "05_website_members_management.png"))

        # 6. Audit Logs
        print("[+] Chụp ảnh 06: Nhật ký kiểm toán (Audit Logs)...")
        driver.get("https://localhost:8443/audit")
        time.sleep(2)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "06_website_audit_logs.png"))

        # 7. pgAdmin 4
        print("[*] Đang truy cập pgAdmin tại http://localhost:8081...")
        try:
            driver.get("http://localhost:8081")
            time.sleep(5)
            # Nếu có màn hình login pgAdmin
            email_fields = driver.find_elements(By.NAME, "email")
            if email_fields:
                email_fields[0].send_keys("admin@pm.local")
                # Đọc mật khẩu pgadmin từ .env nếu có
                with open(".env") as f:
                    for line in f:
                        if line.startswith("PGADMIN_DEFAULT_PASSWORD="):
                            pg_pass = line.strip().split("=")[1]
                            driver.find_element(By.NAME, "password").send_keys(pg_pass)
                            break
                driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
                time.sleep(5)
            driver.save_screenshot(os.path.join(EVIDENCE_DIR, "07_pgadmin_database.png"))
            print("[+] Chụp ảnh 07: pgAdmin 4 thành công.")
        except Exception as e:
            print(f"[-] pgAdmin screenshot warning: {e}")

        # 8. Prometheus Targets
        print("[*] Đang truy cập Prometheus Targets tại http://localhost:9090/targets...")
        driver.get("http://localhost:9090/targets")
        time.sleep(3)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "08_prometheus_targets.png"))
        print("[+] Chụp ảnh 08: Prometheus Targets thành công.")

        # 9. Grafana Dashboard
        print("[*] Đang truy cập Grafana tại http://localhost:3002...")
        # Đọc mật khẩu grafana từ .env
        grafana_pass = ""
        with open(".env") as f:
            for line in f:
                if line.startswith("GRAFANA_ADMIN_PASSWORD="):
                    grafana_pass = line.strip().split("=")[1]
                    break

        driver.get("http://localhost:3002/login")
        time.sleep(2)
        try:
            user_elem = driver.find_element(By.NAME, "user")
            pass_elem = driver.find_element(By.NAME, "password")
            user_elem.send_keys("admin")
            pass_elem.send_keys(grafana_pass)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(3)
        except Exception:
            pass

        # Mở Dashboard Project Management
        print("[+] Chụp ảnh 09: Grafana Overview Dashboard...")
        driver.get("http://localhost:3002/d/pm-overview-dashboard/he-thong-quan-ly-du-an-container-web-database?orgId=1&refresh=5s")
        time.sleep(6)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "09_grafana_dashboard.png"))

        # 10. Grafana Explore - LogQL Query 1: Nginx Access
        print("[+] Chụp ảnh 10: LogQL Query 1 {job=\"nginx\"}...")
        driver.get('http://localhost:3002/explore?schemaVersion=1&panes=%7B%22v0%22:%7B%22datasource%22:%22loki%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob%3D%5C%22nginx%5C%22%7D%22,%22queryType%22:%22range%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1')
        time.sleep(6)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "10_grafana_loki_query1_access.png"))

        # 11. Grafana Explore - LogQL Query 2: HTTP Errors >= 400
        print("[+] Chụp ảnh 11: LogQL Query 2 {job=\"nginx\"} | json | status >= 400...")
        driver.get('http://localhost:3002/explore?schemaVersion=1&panes=%7B%22v0%22:%7B%22datasource%22:%22loki%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob%3D%5C%22nginx%5C%22%7D%20%7C%20json%20%7C%20status%20%3E%3D%20400%22,%22queryType%22:%22range%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1')
        time.sleep(6)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "11_grafana_loki_query2_errors.png"))

        # 12. Grafana Explore - LogQL Query 3: App Security Events
        print("[+] Chụp ảnh 12: LogQL Query 3 {job=\"app\"} | json | event=\"login_failed\"...")
        driver.get('http://localhost:3002/explore?schemaVersion=1&panes=%7B%22v0%22:%7B%22datasource%22:%22loki%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob%3D%5C%22app%5C%22%7D%20%7C%20json%20%7C%20event%3D%5C%22login_failed%5C%22%22,%22queryType%22:%22range%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1')
        time.sleep(6)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "12_grafana_loki_query3_login_failed.png"))

        # 13. GitHub Repository
        print("[+] Chụp ảnh 13: GitHub Repository...")
        driver.get("https://github.com/dtc245220019-create/ProjectManagement_TKQTHT")
        time.sleep(3)
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "13_github_repository.png"))

        print("=" * 70)
        print("[+] ĐÃ HOÀN TẤT CHỤP TOÀN BỘ 13 ẢNH MINH CHỨNG THẬT TRONG docs/evidence/!")
        print("=" * 70)
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_all()
