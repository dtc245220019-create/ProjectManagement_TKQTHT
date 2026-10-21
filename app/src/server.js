require('dotenv').config();
const path = require('path');
const express = require('express');
const session = require('express-session');
const pgSession = require('connect-pg-simple')(session);
const { pool } = require('./config/db');
const logger = require('./config/logger');
const { helmetMiddleware, globalLimiter } = require('./middleware/security');
const { populateUser } = require('./middleware/auth');
const csrfProtection = require('./middleware/csrf');

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

// Trust first proxy (Nginx reverse proxy)
app.set('trust proxy', 1);

// Cấu hình View Engine: EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../views'));

// Static assets (CSS, JS, Images)
app.use(express.static(path.join(__dirname, '../public')));

// Security Headers qua Helmet
app.use(helmetMiddleware);

// Body parsing
app.use(express.urlencoded({ extended: true, limit: '100kb' }));
app.use(express.json({ limit: '100kb' }));

// Global Rate Limiter
app.use(globalLimiter);

// Cấu hình Session lưu trong PostgreSQL bằng connect-pg-simple
app.use(
  session({
    store: new pgSession({
      pool,
      tableName: 'session',
      createTableIfMissing: true
    }),
    secret: process.env.SESSION_SECRET || 'dev_secret_long_key_project_management_2026',
    resave: false,
    saveUninitialized: false,
    name: 'pm_session_id',
    cookie: {
      httpOnly: true,
      secure: process.env.COOKIE_SECURE === 'true',
      sameSite: 'lax',
      maxAge: 24 * 60 * 60 * 1000 // 24 giờ
    }
  })
);

// Population of View Globals & CSRF Protection
app.use(populateUser);
app.use(csrfProtection);

// HTTP Access Logging Middleware (JSON format cho Promtail/Loki)
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    // Bỏ qua log truy cập tĩnh để tránh nhiễu
    if (!req.path.startsWith('/css') && !req.path.startsWith('/js') && !req.path.startsWith('/favicon')) {
      logger.info('http_request', `${req.method} ${req.originalUrl} ${res.statusCode} ${duration}ms`, {
        method: req.method,
        path: req.originalUrl,
        status: res.statusCode,
        duration_ms: duration,
        ip: req.ip,
        user: req.session?.user?.username || 'anonymous'
      });
    }
  });
  next();
});

// Import Routes
const indexRouter = require('./routes/index');
const authRouter = require('./routes/auth');
const projectsRouter = require('./routes/projects');
const tasksRouter = require('./routes/tasks');
const membersRouter = require('./routes/members');

// Register Routes
app.use('/', indexRouter);
app.use('/', authRouter);
app.use('/projects', projectsRouter);
app.use('/tasks', tasksRouter);
app.use('/members', membersRouter);

// 404 Handler
app.use((req, res) => {
  logger.warn('http_404', `Resource not found: ${req.method} ${req.originalUrl}`, {
    method: req.method,
    path: req.originalUrl,
    ip: req.ip
  });

  if (req.xhr || req.headers.accept?.includes('application/json')) {
    return res.status(404).json({ error: 'Endpoint not found.' });
  }

  res.status(404).render('error', {
    title: '404 - Không tìm thấy trang',
    statusCode: 404,
    message: 'Trang bạn đang tìm kiếm không tồn tại hoặc đã được di chuyển.'
  });
});

// Global Error Handler
app.use((err, req, res, next) => {
  logger.error('server_error', `Unhandled application error: ${err.message}`, {
    error: err.message,
    stack: err.stack,
    method: req.method,
    path: req.originalUrl
  });

  if (req.xhr || req.headers.accept?.includes('application/json')) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }

  res.status(500).render('error', {
    title: '500 - Lỗi máy chủ',
    statusCode: 500,
    message: 'Đã xảy ra lỗi hệ thống. Vui lòng liên hệ quản trị viên.'
  });
});

const server = app.listen(PORT, () => {
  logger.info('app_start', `Project Management Server started on port ${PORT}`, {
    port: PORT,
    node_env: process.env.NODE_ENV || 'development'
  });
});

// Graceful Shutdown
function gracefulShutdown(signal) {
  logger.info('app_shutdown', `Received ${signal}, shutting down gracefully...`);
  server.close(async () => {
    try {
      await pool.end();
      logger.info('app_shutdown', 'Database pool closed successfully.');
      process.exit(0);
    } catch (err) {
      logger.error('app_shutdown_error', 'Error closing database pool', { error: err.message });
      process.exit(1);
    }
  });
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

module.exports = app;
