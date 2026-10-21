# HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT SYSTEM)
### Đề tài số 14 - Học phần: Triển khai và Quản trị Hệ thống Phần mềm

* **Sinh viên thực hiện:** Đinh Gia Bảo
* **Mã sinh viên:** DTC245220019
* **Lớp:** An toàn Thông tin K23A (ATTT K23A)
* **Giảng viên hướng dẫn:** ThS. Nguyễn Anh Chuyên
* **Trường:** Đại học Công nghệ Thông tin & Truyền thông - Đại học Thái Nguyên (ICTU)
* **Repository:** [https://github.com/dtc245220019-create/ProjectManagement_TKQTHT.git](https://github.com/dtc245220019-create/ProjectManagement_TKQTHT.git)

---

## 1. Giới thiệu Tổng quan

Hệ thống Quản lý Dự án (Project Management) là giải pháp quản lý toàn diện các dự án phát triển phần mềm, phân công nhiệm vụ (tasks), theo dõi tiến độ và quản lý thành viên đội ngũ kỹ thuật. Hệ thống được thiết kế theo kiến trúc Microservices đóng gói bằng **Docker Compose**, phân tách mạng chặt chẽ, tiếp nhận lưu lượng qua **Nginx Reverse Proxy (TLS)**, cơ sở dữ liệu **PostgreSQL** kết hợp công cụ quản trị **pgAdmin**, hệ thống giám sát thời gian thực **Prometheus + Grafana**, và hệ thống lưu trữ log tập trung **Loki + Promtail**.

### Bảng phân bổ dịch vụ và cổng truy cập:

| Dịch vụ | Image / Nền tảng | Cổng Host (127.0.0.1) | Cổng Container | Vai trò & Mục đích |
| :--- | :--- | :--- | :--- | :--- |
| **pm-app** | Node.js 22 LTS (Alpine) | *Không publish* | `3000` | Ứng dụng quản trị dự án, task, thành viên, audit logs |
| **pm-postgres** | PostgreSQL 16 (Alpine) | *Không publish* | `5432` | CSDL quan hệ chính (mạng database internal) |
| **pm-pgadmin** | dpage/pgadmin4:8.14 | `8081` | `80` | Giao diện đồ họa quản trị CSDL PostgreSQL |
| **pm-nginx** | Nginx 1.27 (Alpine) | `8080`, `8443` | `8080`, `8443`, `8082` | Reverse Proxy, chuyển hướng HTTP sang HTTPS, TLS tự ký |
| **pm-cadvisor** | google/cadvisor:v0.55.1 | *Không publish* | `8080` | Thu thập metrics CPU, RAM, Network container |
| **pm-postgres-exporter**| prometheuscommunity/postgres-exporter | *Không publish* | `9187` | Thu thập chỉ số hiệu năng PostgreSQL |
| **pm-nginx-exporter** | nginx/nginx-prometheus-exporter:1.4.1 | *Không publish* | `9113` | Đọc stub_status Nginx xuất metrics |
| **pm-prometheus** | prom/prometheus:v3.2.1 | `9090` | `9090` | Thu thập, lưu trữ time-series metrics 4 targets |
| **pm-grafana** | grafana/grafana:11.5.0 | `3002` | `3000` | Trực quan hóa dashboard giám sát & truy vấn LogQL |
| **pm-loki** | grafana/loki:3.4.2 | *Không publish* | `3100` | Lưu trữ và lập chỉ mục log tập trung (TSDB schema) |
| **pm-promtail** | grafana/promtail:3.4.2 | *Không publish* | `9080` | Thu gom JSON log từ Nginx và App đẩy về Loki |
| **pm-init-logs** | busybox:1.37.0 | *Không publish* | - | Thiết lập phân quyền UID volumes rồi thoát (code 0) |

---

## 2. Các Biện pháp An toàn Hệ thống (Hardening)

1. **Non-Root Execution:** Container ứng dụng `pm-app` chạy dưới tài khoản unprivileged `node` (`UID 1000: GID 1000`). Nginx worker chạy dưới `UID 101`. Loki và Promtail chạy dưới `UID 10001`.
2. **Network Isolation & Internal Database:** Cơ sở dữ liệu PostgreSQL nằm trọn vẹn trong mạng bridge `pm_database_network` có thuộc tính `internal: true`. Cổng `5432` tuyệt đối không publish ra ngoài máy chủ host.
3. **Localhost Binding:** Toàn bộ các cổng dịch vụ phục vụ môi trường demo (`8080`, `8443`, `8081`, `9090`, `3002`) đều được bind tường minh vào `127.0.0.1` thay vì `0.0.0.0`.
4. **Least-Privilege Database User:** Ứng dụng kết nối bằng tài khoản `pm_app` chỉ có quyền CRUD trên các bảng và sequences cần thiết; không có quyền `DROP TABLE`, `ALTER TABLE` hay `CREATE DATABASE`. Tài khoản `postgres_exporter` được gán quyền đọc `pg_monitor`.
5. **Read-Only Root Filesystem:** Container ứng dụng được bật cờ `read_only: true`, vô hiệu hóa quyền ghi vào hệ điều hành container. Thư mục tạm `/tmp` dùng `tmpfs:rw,noexec,nosuid,size=64m`.
6. **Capability Dropping & Privilege Escalation Prevention:** Áp dụng `cap_drop: [ALL]` và `security_opt: [no-new-privileges:true]` cho container `pm-app` và các dịch vụ liên quan.
7. **Secrets Management:** File bí mật `.env`, khóa riêng tư `certs/*.key`, và file sao lưu `backups/*.sql` được loại trừ hoàn toàn khỏi Git qua `.gitignore`. File `scripts/setup.py` tự động sinh mật khẩu ngẫu nhiên có độ dài và độ phức tạp cao.
8. **Web Security Headers & CSRF Protection:** Tích hợp `Helmet` và Nginx security headers (`nosniff`, `DENY`, `strict-origin-when-cross-origin`, `Strict-Transport-Security`, `Content-Security-Policy`), chống tấn công CSRF bằng token đồng bộ, giới hạn tốc độ truy cập `express-rate-limit`, và cờ bảo mật cookie `HttpOnly`, `SameSite=Lax`, `Secure`.

---

## 3. Hướng dẫn Khởi chạy và Tái lập Hệ thống

### 3.1. Chuẩn bị môi trường
Yêu cầu máy chủ hoặc máy thực nghiệm cài đặt:
* **Docker Desktop** (Engine 24+ hoặc 28+) và **Docker Compose v2**
* **Python 3.10+** (có sẵn thư viện `cryptography` để sinh chứng chỉ SSL)

### 3.2. Cấu hình biến môi trường và chứng chỉ TLS
Chạy script tự động khởi tạo:
```bash
python scripts/setup.py
```
Script sẽ tự động:
1. Tạo file `.env` chứa mật khẩu ngẫu nhiên cho PostgreSQL, pgAdmin, App, Exporter và Grafana.
2. Sinh cặp khóa TLS tự ký `server.key` và `server.crt` (RSA 3072 bit, SHA-256, SAN `localhost`, `127.0.0.1`) trong thư mục `certs/`.

### 3.3. Khởi chạy toàn bộ hệ thống
Khởi chạy kết hợp cả 3 file Compose:
```bash
docker compose -f compose.yaml -f compose.monitoring.yaml -f compose.logging.yaml up -d --build
```

Kiểm tra trạng thái các container:
```bash
docker compose -f compose.yaml -f compose.monitoring.yaml -f compose.logging.yaml ps
```

---

## 4. Địa chỉ Truy cập và Tài khoản Đăng nhập

| Dịch vụ | URL Truy cập | Tài khoản / Mật khẩu |
| :--- | :--- | :--- |
| **Website (HTTPS)** | [https://localhost:8443](https://localhost:8443) | `admin` / `Admin@ProjectMgmt2026!` |
| **Website (HTTP Redirect)**| [http://localhost:8080](http://localhost:8080) | Tự động chuyển hướng sang HTTPS 8443 |
| **Health Check API** | [https://localhost:8443/health](https://localhost:8443/health) | Công khai (trả JSON UP & DB CONNECTED) |
| **pgAdmin 4** | [http://localhost:8081](http://localhost:8081) | Email: `admin@pm.local` / Mật khẩu: xem trong `.env` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Không yêu cầu đăng nhập (xem targets tại `/targets`) |
| **Grafana** | [http://localhost:3002](http://localhost:3002) | `admin` / Mật khẩu: xem trong `.env` |

---

## 5. Quy trình Kiểm thử, Sao lưu và Phục hồi

### 5.1. Chạy Smoke Test kiểm tra hệ thống
```bash
python scripts/smoke_test.py
```
Script tự động kiểm tra:
* Kết nối HTTP/HTTPS, kiểm tra chuyển hướng 301
* Kiểm tra tính hợp lệ của Header bảo mật (`nosniff`, `DENY`)
* Kiểm tra API `/health` (xác nhận trạng thái PostgreSQL)
* Thử nghiệm đăng nhập đúng, đăng nhập sai, chống CSRF và kiểm tra các thao tác CRUD.

### 5.2. Sao lưu cơ sở dữ liệu (Backup)
```bash
python scripts/backup.py
```
Dữ liệu được trích xuất bằng `pg_dump` vào file `backups/pm_db_backup_<timestamp>.sql`.

### 5.3. Phục hồi kiểm chứng độc lập (Restore Test)
```bash
python scripts/restore_test.py backups/<tên_file_dump>.sql
```
Script tự động tạo một cơ sở dữ liệu độc lập `pm_restore_test`, nạp file backup và đối chiếu số lượng bản ghi giữa database chính và database phục hồi nhằm đảm bảo toàn vẹn dữ liệu mà không làm gián đoạn hệ thống đang chạy.
