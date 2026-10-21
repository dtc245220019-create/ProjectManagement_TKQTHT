const express = require('express');
const router = express.Router();
const Member = require('../models/member');
const Audit = require('../models/audit');
const { isAuthenticated, requireRole } = require('../middleware/auth');
const logger = require('../config/logger');

// Danh sách thành viên
router.get('/', isAuthenticated, async (req, res) => {
  try {
    const members = await Member.getAllMembers();
    res.render('members/list', {
      title: 'Quản lý Thành viên',
      members,
      error: null
    });
  } catch (err) {
    logger.error('members_fetch_error', 'Failed to fetch members', { error: err.message });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể tải danh sách thành viên.' });
  }
});

// Trang thêm thành viên mới
router.get('/new', isAuthenticated, requireRole('admin', 'manager'), (req, res) => {
  res.render('members/new', {
    title: 'Thêm Thành viên Mới',
    error: null,
    formData: {}
  });
});

// Xử lý thêm thành viên mới (POST)
router.post('/', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const { full_name, email, role, department, phone, status } = req.body;

  if (!full_name || !email || !role || !department) {
    return res.status(400).render('members/new', {
      title: 'Thêm Thành viên Mới',
      error: 'Vui lòng điền đầy đủ Họ tên, Email, Vai trò và Phòng ban.',
      formData: req.body
    });
  }

  try {
    const created = await Member.createMember({
      full_name: full_name.trim(),
      email: email.trim().toLowerCase(),
      role: role.trim(),
      department: department.trim(),
      phone: phone ? phone.trim() : null,
      status: status || 'Active'
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'CREATE_MEMBER',
      entityType: 'MEMBER',
      entityId: created.id,
      details: { name: created.full_name, email: created.email },
      ip: req.ip
    });

    res.redirect('/members');
  } catch (err) {
    logger.error('create_member_error', 'Failed to create member', { error: err.message });
    res.status(500).render('members/new', {
      title: 'Thêm Thành viên Mới',
      error: 'Không thể tạo thành viên: ' + (err.code === '23505' ? 'Email đã tồn tại.' : err.message),
      formData: req.body
    });
  }
});

// Cập nhật thông tin thành viên (POST)
router.post('/:id/edit', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const memberId = parseInt(req.params.id, 10);
  const { full_name, email, role, department, phone, status } = req.body;

  try {
    const updated = await Member.updateMember(memberId, {
      full_name: full_name.trim(),
      email: email.trim().toLowerCase(),
      role: role.trim(),
      department: department.trim(),
      phone: phone ? phone.trim() : null,
      status: status || 'Active'
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'UPDATE_MEMBER',
      entityType: 'MEMBER',
      entityId: memberId,
      details: { name: updated.full_name, role: updated.role, status: updated.status },
      ip: req.ip
    });

    res.redirect('/members');
  } catch (err) {
    logger.error('update_member_error', 'Failed to update member', { error: err.message, memberId });
    res.redirect('/members?error=update_failed');
  }
});

// Xóa thành viên (POST)
router.post('/:id/delete', isAuthenticated, requireRole('admin'), async (req, res) => {
  const memberId = parseInt(req.params.id, 10);

  try {
    const deleted = await Member.deleteMember(memberId);
    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'DELETE_MEMBER',
      entityType: 'MEMBER',
      entityId: memberId,
      details: { name: deleted?.full_name },
      ip: req.ip
    });

    res.redirect('/members');
  } catch (err) {
    logger.error('delete_member_error', 'Failed to delete member', { error: err.message, memberId });
    res.redirect('/members?error=delete_failed');
  }
});

module.exports = router;
