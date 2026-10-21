const { Pool } = require('pg');
const logger = require('./logger');

const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'postgres',
  port: parseInt(process.env.POSTGRES_PORT || '5432', 10),
  database: process.env.POSTGRES_DB || 'pm_db',
  user: process.env.APP_DB_USER || 'pm_app',
  password: process.env.APP_DB_PASSWORD || 'AppUserSecretPassword2026!',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('connect', () => {
  // Connection successfully acquired
});

pool.on('error', (err) => {
  logger.error('db_pool_error', 'Unexpected error on idle database client', {
    error: err.message,
    stack: err.stack
  });
});

async function query(text, params) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    if (process.env.NODE_ENV !== 'production') {
      logger.info('db_query', 'Executed query', { duration, rows: res.rowCount });
    }
    return res;
  } catch (err) {
    const duration = Date.now() - start;
    logger.error('db_query_error', 'Database query execution failed', {
      duration,
      query: text,
      error: err.message
    });
    throw err;
  }
}

async function checkHealth() {
  try {
    const res = await pool.query('SELECT 1 AS ok, current_database() AS db, current_user AS usr');
    return {
      status: 'CONNECTED',
      database: res.rows[0].db,
      user: res.rows[0].usr,
      pool: {
        total: pool.totalCount,
        idle: pool.idleCount,
        waiting: pool.waitingCount
      }
    };
  } catch (err) {
    return {
      status: 'DISCONNECTED',
      error: err.message
    };
  }
}

module.exports = {
  pool,
  query,
  checkHealth
};
