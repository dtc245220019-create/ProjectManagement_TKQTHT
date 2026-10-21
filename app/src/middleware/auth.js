const logger = require('../config/logger');

function isAuthenticated(req, res, next) {
  if (req.session && req.session.user) {
    return next();
  }

  if (req.xhr || req.headers.accept?.includes('application/json')) {
    return res.status(401).json({ error: 'Unauthorized. Please login.' });
  }

  logger.warn('auth_unauthorized', 'Unauthorized access attempt redirected to login', {
    path: req.originalUrl,
    ip: req.ip
  });
  return res.redirect('/login?redirect=' + encodeURIComponent(req.originalUrl));
}

function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.session || !req.session.user) {
      return res.status(401).redirect('/login');
    }

    const userRole = req.session.user.role;
    if (roles.includes(userRole) || userRole === 'admin') {
      return next();
    }

    logger.warn('auth_forbidden', 'Access forbidden due to insufficient role permissions', {
      user: req.session.user.username,
      userRole,
      requiredRoles: roles,
      path: req.originalUrl
    });

    if (req.xhr || req.headers.accept?.includes('application/json')) {
      return res.status(403).json({ error: 'Forbidden: Insufficient privileges.' });
    }

    return res.status(403).render('error', {
      title: 'Truy cập bị từ chối - 403 Forbidden',
      statusCode: 403,
      message: 'Bạn không có đủ quyền hạn để thực hiện thao tác này.'
    });
  };
}

function populateUser(req, res, next) {
  res.locals.currentUser = req.session ? req.session.user : null;
  res.locals.currentPath = req.path;
  next();
}

module.exports = {
  isAuthenticated,
  requireRole,
  populateUser
};
