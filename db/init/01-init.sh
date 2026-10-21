#!/bin/sh
set -e

# ==============================================================================
# Script 01-init.sh: Khởi tạo Role và User đặc quyền tối thiểu trong PostgreSQL
# ==============================================================================

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- 1. Tạo user ứng dụng pm_app với quyền tối thiểu
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_DB_USER') THEN
            CREATE ROLE $APP_DB_USER WITH LOGIN PASSWORD '$APP_DB_PASSWORD';
            RAISE NOTICE 'Role % created successfully.', '$APP_DB_USER';
        END IF;
    END
    \$\$;

    -- 2. Tạo user postgres_exporter phục vụ Prometheus monitoring
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$EXPORTER_DB_USER') THEN
            CREATE ROLE $EXPORTER_DB_USER WITH LOGIN PASSWORD '$EXPORTER_DB_PASSWORD';
            GRANT pg_monitor TO $EXPORTER_DB_USER;
            RAISE NOTICE 'Role % created and granted pg_monitor.', '$EXPORTER_DB_USER';
        END IF;
    END
    \$\$;
EOSQL
