const crypto = require('crypto');
const logger = require('../config/logger');

function csrfProtection(req, res, next) {
  if (!req.session) {
    return next();
  }

  // Ensure CSRF token exists in session
  if (!req.session.csrfToken) {
    req.session.csrfToken = crypto.randomBytes(24).toString('hex');
  }

  // Expose token to all views
  res.locals.csrfToken = req.session.csrfToken;

  // Safe HTTP methods don't require CSRF validation
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next();
  }

  // Exempt internal healthcheck / API if configured
  if (req.path === '/health' || req.path === '/api/health') {
    return next();
  }

  const clientToken = req.body?._csrf || req.headers['x-csrf-token'] || req.headers['csrf-token'];

  if (!clientToken || clientToken !== req.session.csrfToken) {
    logger.warn('csrf_denied', 'CSRF validation failed for state-changing request', {
      method: req.method,
      path: req.originalUrl,
      ip: req.ip,
      hasToken: Boolean(clientToken)
    });

    if (req.xhr || req.headers.accept?.includes('application/json')) {
      return res.status(403).json({ error: 'CSRF token mismatch or missing.' });
    }

    return res.status(403).render('error', {
      title: 'Lỗi bảo mật CSRF - 403 Forbidden',
      statusCode: 403,
      message: 'Mã xác thực bảo mật (CSRF Token) không hợp lệ hoặc đã hết hạn. Vui lòng thử tải lại trang.',
      currentUser: req.session ? req.session.user : null,
      currentPath: req.path
    });
  }

  next();
}

module.exports = csrfProtection;
