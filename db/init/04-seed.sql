-- ==============================================================================
-- 04-seed.sql: Dữ liệu mẫu khởi tạo cho Hệ thống Quản lý Dự án (Đề 14)
-- ==============================================================================

-- 1. Seed Users (Mật khẩu mặc định: Admin@ProjectMgmt2026!)
INSERT INTO users (id, username, email, password_hash, role) VALUES
(1, 'admin', 'dtc245220019@ictu.edu.vn', '$2b$10$qhiYkd0k2aFayAty2EKW7.ihfKktHK9AWGLWbSF7OiN7xRroXIIum', 'admin'),
(2, 'giabao', 'dinhgiabao.attt@pm.local', '$2b$10$qhiYkd0k2aFayAty2EKW7.ihfKktHK9AWGLWbSF7OiN7xRroXIIum', 'manager'),
(3, 'developer', 'dev@pm.local', '$2b$10$qhiYkd0k2aFayAty2EKW7.ihfKktHK9AWGLWbSF7OiN7xRroXIIum', 'user')
ON CONFLICT (id) DO NOTHING;

-- Đồng bộ sequence users_id_seq
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- 2. Seed Members
INSERT INTO members (id, user_id, full_name, email, role, department, phone, status) VALUES
(1, 2, 'Đinh Gia Bảo', 'dtc245220019@ictu.edu.vn', 'Project Manager & Tech Lead', 'An toàn Thông tin', '0987654321', 'Active'),
(2, 3, 'Nguyễn Văn An', 'nguyenvanan.dev@pm.local', 'Senior Backend Developer', 'Phát triển Phần mềm', '0912345678', 'Active'),
(3, NULL, 'Trần Thị Bình', 'tranthibinh.fe@pm.local', 'Frontend Developer', 'Phát triển Phần mềm', '0923456789', 'Active'),
(4, NULL, 'Lê Văn Cường', 'levancuong.qa@pm.local', 'QA & Security Engineer', 'Đảm bảo Chất lượng', '0934567890', 'Active'),
(5, NULL, 'Phạm Hoàng Dũng', 'phamhoangdung.ops@pm.local', 'DevOps & SRE Engineer', 'Hạ tầng & Vận hành', '0945678901', 'Active')
ON CONFLICT (id) DO NOTHING;

SELECT setval('members_id_seq', (SELECT MAX(id) FROM members));

-- 3. Seed Projects
INSERT INTO projects (id, code, name, description, status, priority, start_date, end_date, budget, manager_id) VALUES
(1, 'PRJ-001', 'Hệ thống Quản lý Dự án (Project Management)', 'Triển khai hệ thống phần mềm quản lý dự án, task, thành viên tích hợp PostgreSQL, Nginx, Prometheus, Grafana và Loki theo Đề 14.', 'In Progress', 'Critical', '2026-10-01', '2026-10-30', 50000000.00, 1),
(2, 'PRJ-002', 'Hệ thống Bán vé Xe bus Thông minh (Bus Ticketing)', 'Xây dựng nền tảng đặt vé xe buýt trực tuyến, quản lý tuyến xe, phân công lịch trình tài xế và thanh toán số.', 'Planning', 'High', '2026-11-01', '2026-12-31', 80000000.00, 1),
(3, 'PRJ-003', 'Hạ tầng Tự động hóa CI/CD & Security Hardening', 'Thiết lập pipeline kiểm tra mã nguồn tự động, quét lỗ hổng container, áp dụng các kỹ thuật bảo mật non-root và network isolation.', 'Completed', 'High', '2026-09-01', '2026-09-28', 35000000.00, 1),
(4, 'PRJ-004', 'Nền tảng Giám sát & Quản trị Tập trung Multi-Agent AI', 'Nghiên cứu và triển khai hệ thống điều phối đa tác tử thông minh hỗ trợ phân tích dữ liệu và ra quyết định thời gian thực.', 'On Hold', 'Medium', '2026-08-15', '2026-11-15', 120000000.00, 1)
ON CONFLICT (id) DO NOTHING;

SELECT setval('projects_id_seq', (SELECT MAX(id) FROM projects));

-- 4. Seed Project_Members
INSERT INTO project_members (project_id, member_id, project_role) VALUES
(1, 1, 'Project Manager'),
(1, 2, 'Backend Architect'),
(1, 3, 'Frontend Lead'),
(1, 4, 'Security Tester'),
(1, 5, 'DevOps Specialist'),
(2, 1, 'Technical Advisor'),
(2, 2, 'Core Backend Dev'),
(2, 3, 'Mobile/Web UI Dev'),
(3, 1, 'Security Lead'),
(3, 5, 'DevOps Lead')
ON CONFLICT (project_id, member_id) DO NOTHING;

-- 5. Seed Tasks
INSERT INTO tasks (id, project_id, title, description, status, priority, assigned_to, due_date, estimated_hours, actual_hours) VALUES
(1, 1, 'Thiết kế cơ sở dữ liệu PostgreSQL và pgAdmin', 'Xây dựng schema gồm 7 bảng, thiết lập ràng buộc toàn vẹn, chỉ mục và phân quyền tối thiểu pm_app.', 'Done', 'High', 1, '2026-10-05', 16.0, 14.5),
(2, 1, 'Đóng gói ứng dụng và cấu hình Nginx Reverse Proxy', 'Tạo Dockerfile tối ưu kích thước, cấu hình Nginx chuyển tiếp, bảo vệ HTTP security headers và HTTPS tự ký.', 'Done', 'Critical', 5, '2026-10-10', 20.0, 18.0),
(3, 1, 'Tích hợp giám sát Prometheus và Dashboard Grafana', 'Thu thập metrics từ cadvisor, postgres_exporter, nginx_exporter và cấu hình bảng điều khiển Grafana trực quan.', 'Done', 'High', 5, '2026-10-15', 24.0, 22.0),
(4, 1, 'Thiết lập Log tập trung Loki và Promtail', 'Thu thập log truy cập Nginx, log ứng dụng JSON và kiểm chứng 3 truy vấn LogQL phục vụ vận hành an toàn.', 'Done', 'High', 4, '2026-10-18', 18.0, 16.0),
(5, 1, 'Thực hiện kiểm thử sao lưu và phục hồi dữ liệu', 'Viết kịch bản pg_dump và restore tự động vào database độc lập pm_restore_test, đối chiếu checksum.', 'In Progress', 'Medium', 1, '2026-10-22', 12.0, 8.0),
(6, 1, 'Hoàn thiện báo cáo khoa học cuối kỳ theo mẫu', 'Biên soạn tài liệu Word chi tiết hơn 10 trang, gắn minh chứng thực nghiệm và giải thích kiến trúc.', 'In Progress', 'Critical', 1, '2026-10-23', 30.0, 15.0),
(7, 2, 'Khảo sát nghiệp vụ điều hành xe bus tuyến nội đô', 'Thu thập yêu cầu thực tế từ nhà xe, thiết kế sơ đồ luồng dữ liệu và thiết lập ca sử dụng chính.', 'Todo', 'Medium', 2, '2026-11-10', 40.0, 0.0),
(8, 2, 'Xây dựng API quản lý tuyến đường và định vị GPS', 'Thiết kế RESTful API xử lý tọa độ phương tiện và dự báo thời gian đến trạm xe.', 'Todo', 'High', 2, '2026-11-25', 60.0, 0.0),
(9, 3, 'Cấu hình Docker CIS Benchmark và AppArmor/SecComp', 'Đánh giá an toàn hệ thống container, cấu hình no-new-privileges và cap_drop theo khuyến nghị bảo mật.', 'Done', 'High', 4, '2026-09-20', 16.0, 16.0)
ON CONFLICT (id) DO NOTHING;

SELECT setval('tasks_id_seq', (SELECT MAX(id) FROM tasks));

-- 6. Seed Audit Logs
INSERT INTO audit_logs (user_id, username, action, entity_type, entity_id, details, ip_address) VALUES
(1, 'admin', 'SYSTEM_INITIALIZATION', 'SYSTEM', '0', '{"message": "Cơ sở dữ liệu Hệ thống Quản lý Dự án được khởi tạo thành công."}', '127.0.0.1'),
(1, 'admin', 'LOGIN_SUCCESS', 'AUTH', '1', '{"method": "password", "role": "admin"}', '127.0.0.1'),
(1, 'admin', 'CREATE_PROJECT', 'PROJECT', '1', '{"code": "PRJ-001", "name": "Hệ thống Quản lý Dự án"}', '127.0.0.1');
