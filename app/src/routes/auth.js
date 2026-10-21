const express = require('express');
const router = express.Router();
const User = require('../models/user');
const Audit = require('../models/audit');
const logger = require('../config/logger');
const { loginLimiter } = require('../middleware/security');

router.get('/login', (req, res) => {
  if (req.session && req.session.user) {
    return res.redirect('/');
  }
  res.render('auth/login', {
    title: 'Đăng nhập hệ thống Quản lý Dự án',
    error: req.query.error || null,
    redirect: req.query.redirect || '/',
    username: ''
  });
});

router.post('/login', loginLimiter, async (req, res) => {
  const { username, password, redirect } = req.body;
  const ip = req.ip || req.connection.remoteAddress;

  if (!username || !password) {
    return res.status(400).render('auth/login', {
      title: 'Đăng nhập hệ thống',
      error: 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.',
      redirect: redirect || '/',
      username: username || ''
    });
  }

  try {
    const user = await User.findByUsername(username.trim());
    if (!user) {
      logger.warn('login_failed', 'Failed login attempt - user not found', {
        username,
        ip
      });
      await Audit.logAction({
        username,
        action: 'LOGIN_FAILED',
        entityType: 'AUTH',
        details: { reason: 'User not found' },
        ip
      });
      return res.status(401).render('auth/login', {
        title: 'Đăng nhập hệ thống',
        error: 'Tên đăng nhập hoặc mật khẩu không chính xác.',
        redirect: redirect || '/',
        username
      });
    }

    const isValid = await User.verifyPassword(password, user.password_hash);
    if (!isValid) {
      logger.warn('login_failed', 'Failed login attempt - invalid password', {
        username,
        userId: user.id,
        ip
      });
      await Audit.logAction({
        userId: user.id,
        username: user.username,
        action: 'LOGIN_FAILED',
        entityType: 'AUTH',
        details: { reason: 'Invalid password' },
        ip
      });
      return res.status(401).render('auth/login', {
        title: 'Đăng nhập hệ thống',
        error: 'Tên đăng nhập hoặc mật khẩu không chính xác.',
        redirect: redirect || '/',
        username
      });
    }

    // Regenerate session to prevent session fixation attacks
    req.session.regenerate((err) => {
      if (err) {
        logger.error('session_error', 'Session regeneration failed', { error: err.message });
        return res.status(500).send('Internal Server Error');
      }

      req.session.user = {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role
      };

      logger.info('login_success', 'User logged in successfully', {
        userId: user.id,
        username: user.username,
        role: user.role,
        ip
      });

      Audit.logAction({
        userId: user.id,
        username: user.username,
        action: 'LOGIN_SUCCESS',
        entityType: 'AUTH',
        entityId: user.id,
        details: { role: user.role },
        ip
      });

      const target = redirect && redirect.startsWith('/') ? redirect : '/';
      res.redirect(target);
    });
  } catch (err) {
    logger.error('login_exception', 'Unexpected error during login process', { error: err.message });
    res.status(500).render('auth/login', {
      title: 'Đăng nhập hệ thống',
      error: 'Đã xảy ra lỗi máy chủ trong quá trình xác thực. Vui lòng thử lại sau.',
      redirect: redirect || '/',
      username
    });
  }
});

router.get('/logout', (req, res) => {
  const user = req.session ? req.session.user : null;
  const ip = req.ip;

  if (user) {
    logger.info('logout', 'User logged out', { userId: user.id, username: user.username, ip });
    Audit.logAction({
      userId: user.id,
      username: user.username,
      action: 'LOGOUT',
      entityType: 'AUTH',
      entityId: user.id,
      ip
    });
  }

  req.session.destroy(() => {
    res.clearCookie('connect.sid');
    res.redirect('/login');
  });
});

module.exports = router;
