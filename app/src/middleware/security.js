const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const logger = require('../config/logger');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 phút
  max: 15, // Tối đa 15 lần thử đăng nhập
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn('login_rate_limited', 'Too many login attempts from IP', {
      ip: req.ip,
      path: req.originalUrl
    });
    res.status(429).render('auth/login', {
      title: 'Đăng nhập hệ thống',
      error: 'Bạn đã thử đăng nhập quá nhiều lần. Vui lòng thử lại sau 15 phút.',
      username: req.body?.username || ''
    });
  }
});

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: parseInt(process.env.RATE_LIMIT_MAX || '500', 10),
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn('rate_limit_exceeded', 'Global rate limit exceeded', {
      ip: req.ip,
      path: req.originalUrl
    });
    res.status(429).json({ error: 'Quá nhiều yêu cầu. Vui lòng thử lại sau.' });
  }
});

const helmetMiddleware = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      fontSrc: ["'self'", "https://cdn.jsdelivr.net"],
      imgSrc: ["'self'", "data:"],
      connectSrc: ["'self'"],
      objectSrc: ["'none'"],
      baseUri: ["'self'"]
    }
  },
  crossOriginEmbedderPolicy: false,
  xContentTypeOptions: true,
  xFrameOptions: { action: 'deny' },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
});

module.exports = {
  loginLimiter,
  globalLimiter,
  helmetMiddleware
};
