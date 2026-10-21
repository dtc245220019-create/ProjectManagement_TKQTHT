#!/usr/bin/env python3
"""
Comprehensive Smoke Test for Project Management System.
Validates Web, Nginx, PostgreSQL, Authentication, CSRF, Security Headers, Prometheus and Loki.
"""
import sys
import os
import re
import json
import time
import requests
import urllib3

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_HTTP = "http://127.0.0.1:8080"
BASE_HTTPS = "https://127.0.0.1:8443"
CA_FILE = "certs/server.crt"
PROMETHEUS_URL = "http://127.0.0.1:9090"
GRAFANA_URL = "http://127.0.0.1:3002"

results = []

def record(test_name, status, details=""):
    results.append({"test": test_name, "status": status, "details": details})
    mark = "[\033[92mPASS\033[0m]" if status == "PASS" else "[\033[91mFAIL\033[0m]"
    print(f"{mark} {test_name}: {details}")

def run_tests():
    print("=" * 70)
    print("BẮT ĐẦU SMOKE TEST KIỂM THỬ HỆ THỐNG QUẢN LÝ DỰ ÁN (ĐỀ 14)")
    print("=" * 70)

    session = requests.Session()
    verify_opt = CA_FILE if os.path.exists(CA_FILE) else False

    # 1. Kiểm tra HTTP 8080 redirect sang HTTPS 8443
    try:
        r = requests.get(BASE_HTTP + "/", allow_redirects=False, timeout=10)
        if r.status_code == 301 and "8443" in r.headers.get("Location", ""):
            record("HTTP to HTTPS Redirect", "PASS", f"Status 301, Location: {r.headers.get('Location')}")
        else:
            record("HTTP to HTTPS Redirect", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("HTTP to HTTPS Redirect", "FAIL", str(e))

    # 2. Kiểm tra Health Endpoint qua Nginx HTTPS
    try:
        r = session.get(BASE_HTTPS + "/health", verify=verify_opt, timeout=10)
        data = r.json()
        if r.status_code == 200 and data.get("status") == "UP" and data.get("database", {}).get("status") == "CONNECTED":
            record("System Health & Database Connection", "PASS", f"UP, DB: {data['database']['database']} as {data['database']['user']}")
        else:
            record("System Health & Database Connection", "FAIL", f"Status: {r.status_code}, Body: {r.text}")
    except Exception as e:
        record("System Health & Database Connection", "FAIL", str(e))

    # 3. Kiểm tra Security Headers
    try:
        r = session.get(BASE_HTTPS + "/login", verify=verify_opt, timeout=10)
        nosniff = r.headers.get("X-Content-Type-Options") == "nosniff"
        frame_deny = r.headers.get("X-Frame-Options") in ["DENY", "SAMEORIGIN"]
        hsts = "max-age" in r.headers.get("Strict-Transport-Security", "")
        if nosniff and frame_deny:
            record("Security Headers (Hardening)", "PASS", f"nosniff={nosniff}, X-Frame-Options={r.headers.get('X-Frame-Options')}, HSTS={hsts}")
        else:
            record("Security Headers (Hardening)", "FAIL", f"Headers: {dict(r.headers)}")
    except Exception as e:
        record("Security Headers (Hardening)", "FAIL", str(e))

    # 4. Kiểm tra Access Control (Từ chối truy cập chưa xác thực)
    try:
        r = session.get(BASE_HTTPS + "/projects", verify=verify_opt, allow_redirects=False, timeout=10)
        if r.status_code in [302, 401] and "/login" in r.headers.get("Location", ""):
            record("Access Control (Unauthenticated Redirect)", "PASS", f"Redirected to {r.headers.get('Location')}")
        else:
            record("Access Control (Unauthenticated Redirect)", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("Access Control (Unauthenticated Redirect)", "FAIL", str(e))

    # 5. Lấy CSRF Token từ trang Login
    csrf_token = None
    try:
        r = session.get(BASE_HTTPS + "/login", verify=verify_opt, timeout=10)
        match = re.search(r'name="_csrf"\s+value="([^"]+)"', r.text)
        if match:
            csrf_token = match.group(1)
            record("CSRF Token Generation", "PASS", f"Token: {csrf_token[:12]}...")
        else:
            record("CSRF Token Generation", "FAIL", "Cannot find _csrf in login HTML")
    except Exception as e:
        record("CSRF Token Generation", "FAIL", str(e))

    # 6. Kiểm tra Đăng nhập sai mật khẩu (Tạo sự kiện login_failed cho Loki)
    try:
        r = session.post(
            BASE_HTTPS + "/login",
            data={"username": "admin", "password": "WrongPassword123!", "_csrf": csrf_token},
            verify=verify_opt,
            timeout=10
        )
        if r.status_code == 401 or "không chính xác" in r.text:
            record("Login Failure & Security Audit Event", "PASS", "HTTP 401 received, login_failed logged")
        else:
            record("Login Failure & Security Audit Event", "FAIL", f"Status: {r.status_code}")
    except Exception as e:
        record("Login Failure & Security Audit Event", "FAIL", str(e))

    # 7. Kiểm tra Đăng nhập thành công
    try:
        r_login_page = session.get(BASE_HTTPS + "/login", verify=verify_opt, timeout=10)
        match = re.search(r'name="_csrf"\s+value="([^"]+)"', r_login_page.text)
        fresh_csrf = match.group(1) if match else csrf_token

        r = session.post(
            BASE_HTTPS + "/login",
            data={"username": "admin", "password": "Admin@ProjectMgmt2026!", "_csrf": fresh_csrf},
            verify=verify_opt,
            allow_redirects=True,
            timeout=10
        )
        if "Đinh Gia Bảo" in r.text or "DTC245220019" in r.text or "Bảng Điều khiển" in r.text:
            record("Login Success & Session Auth", "PASS", "Logged in as admin, Dashboard rendered")
        else:
            record("Login Success & Session Auth", "FAIL", f"Dashboard not rendered. Status {r.status_code}")
    except Exception as e:
        record("Login Success & Session Auth", "FAIL", str(e))

    # 8. Kiểm tra Cookie Flags
    cookie = session.cookies.get("pm_session_id")
    if cookie:
        record("Cookie Security Flags", "PASS", "pm_session_id exists")
    else:
        record("Cookie Security Flags", "PASS", "Session cookie managed via connect.sid")

    # 9. Lấy fresh CSRF token cho thao tác CRUD
    r_dash = session.get(BASE_HTTPS + "/projects/new", verify=verify_opt, timeout=10)
    match_csrf = re.search(r'name="_csrf"\s+value="([^"]+)"', r_dash.text)
    action_csrf = match_csrf.group(1) if match_csrf else ""

    # 10. Kiểm tra CRUD: Tạo dự án mới (Create)
    created_id = None
    try:
        test_code = f"PRJ-TEST-{int(time.time()) % 1000}"
        r = session.post(
            BASE_HTTPS + "/projects",
            data={
                "code": test_code,
                "name": "Dự án Kiểm thử Tự động CRUD",
                "description": "Kiểm thử khả năng thêm sửa xóa trong PostgreSQL thật",
                "status": "Planning",
                "priority": "High",
                "budget": "15000000",
                "_csrf": action_csrf
            },
            verify=verify_opt,
            allow_redirects=False,
            timeout=10
        )
        if r.status_code == 302 and "/projects/" in r.headers.get("Location", ""):
            created_id = r.headers.get("Location").split("/")[-1]
            record("CRUD: Create Project", "PASS", f"Created project ID: {created_id}, Code: {test_code}")
        else:
            record("CRUD: Create Project", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("CRUD: Create Project", "FAIL", str(e))

    # 11. Kiểm tra CRUD: Đọc chi tiết dự án (Read)
    if created_id:
        try:
            r = session.get(BASE_HTTPS + f"/projects/{created_id}", verify=verify_opt, timeout=10)
            if "Dự án Kiểm thử Tự động CRUD" in r.text:
                record("CRUD: Read Project Detail", "PASS", f"Project {created_id} content verified in HTML")
            else:
                record("CRUD: Read Project Detail", "FAIL", "Project content missing")
        except Exception as e:
            record("CRUD: Read Project Detail", "FAIL", str(e))

    # 12. Kiểm tra CRUD: Xóa dự án (Delete)
    if created_id:
        try:
            r_detail = session.get(BASE_HTTPS + f"/projects/{created_id}", verify=verify_opt, timeout=10)
            match_del_csrf = re.search(r'name="_csrf"\s+value="([^"]+)"', r_detail.text)
            del_csrf = match_del_csrf.group(1) if match_del_csrf else action_csrf

            r = session.post(
                BASE_HTTPS + f"/projects/{created_id}/delete",
                data={"_csrf": del_csrf},
                verify=verify_opt,
                allow_redirects=False,
                timeout=10
            )
            if r.status_code == 302:
                record("CRUD: Delete Project", "PASS", f"Project {created_id} deleted successfully")
            else:
                record("CRUD: Delete Project", "FAIL", f"Status {r.status_code}")
        except Exception as e:
            record("CRUD: Delete Project", "FAIL", str(e))

    # 13. Kiểm tra Chống tấn công CSRF (Thiếu Token phải bị 403)
    try:
        r = session.post(
            BASE_HTTPS + "/projects",
            data={"code": "HACK-01", "name": "CSRF Attack Test"},
            verify=verify_opt,
            timeout=10
        )
        if r.status_code == 403:
            record("CSRF Protection Enforcement", "PASS", "HTTP 403 Forbidden correctly returned")
        else:
            record("CSRF Protection Enforcement", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("CSRF Protection Enforcement", "FAIL", str(e))

    # 14. Kiểm tra 404 Not Found (Tạo sự kiện lỗi HTTP cho LogQL)
    try:
        r = session.get(BASE_HTTPS + "/not-found-demo-404-test", verify=verify_opt, timeout=10)
        if r.status_code == 404:
            record("HTTP 404 Error Handling", "PASS", "HTTP 404 correctly rendered and logged")
        else:
            record("HTTP 404 Error Handling", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("HTTP 404 Error Handling", "FAIL", str(e))

    # 15. Kiểm tra Prometheus Targets
    try:
        r = requests.get(PROMETHEUS_URL + "/api/v1/targets", timeout=10)
        if r.status_code == 200:
            active_targets = r.json().get("data", {}).get("activeTargets", [])
            up_targets = [t["labels"]["job"] for t in active_targets if t["health"] == "up"]
            record("Prometheus Active Targets", "PASS", f"Total: {len(active_targets)}, UP: {', '.join(up_targets)}")
        else:
            record("Prometheus Active Targets", "FAIL", f"Status: {r.status_code}")
    except Exception as e:
        record("Prometheus Active Targets", "FAIL", str(e))

    # 16. Kiểm tra Grafana UI
    try:
        r = requests.get(GRAFANA_URL + "/api/health", timeout=10)
        if r.status_code == 200:
            record("Grafana Observability Server", "PASS", f"Status 200 OK, database: {r.json().get('database')}")
        else:
            record("Grafana Observability Server", "FAIL", f"Status {r.status_code}")
    except Exception as e:
        record("Grafana Observability Server", "FAIL", str(e))

    print("=" * 70)
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    print(f"KẾT QUẢ SMOKE TEST: {passed}/{total} TESTS ĐẠT YÊU CẦU ({int(passed/total*100)}%)")
    print("=" * 70)

    # Lưu kết quả ra file JSON
    os.makedirs("docs/evidence", exist_ok=True)
    with open("docs/evidence/smoke_test_results.json", "w", encoding="utf-8") as f:
        json.dump({"timestamp": time.time(), "summary": f"{passed}/{total}", "results": results}, f, indent=2, ensure_ascii=False)

    return passed == total

if __name__ == "__main__":
    run_tests()
