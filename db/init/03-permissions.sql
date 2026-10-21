-- ==============================================================================
-- 03-permissions.sql: Phân quyền đặc quyền tối thiểu (Least Privilege) cho pm_app
-- ==============================================================================

GRANT CONNECT ON DATABASE pm_db TO pm_app;
GRANT USAGE ON SCHEMA public TO pm_app;

-- Cấp quyền thao tác dữ liệu cơ bản (CRUD) trên tất cả các bảng
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pm_app;

-- Cấp quyền sử dụng sequences để tự động tăng khóa chính (SERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pm_app;

-- Đảm bảo các bảng tạo mới trong tương lai cũng áp dụng quyền này
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO pm_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO pm_app;
