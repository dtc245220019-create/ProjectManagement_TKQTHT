const express = require('express');
const router = express.Router();
const Project = require('../models/project');
const Task = require('../models/task');
const Member = require('../models/member');
const Audit = require('../models/audit');
const { isAuthenticated, requireRole } = require('../middleware/auth');
const logger = require('../config/logger');

// Danh sách dự án
router.get('/', isAuthenticated, async (req, res) => {
  try {
    const { status, priority, search } = req.query;
    const projects = await Project.getAllProjects({ status, priority, search });
    res.render('projects/list', {
      title: 'Quản lý Dự án',
      projects,
      filters: { status, priority, search }
    });
  } catch (err) {
    logger.error('projects_fetch_error', 'Failed to fetch projects list', { error: err.message });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể tải danh sách dự án.' });
  }
});

// Trang tạo mới dự án
router.get('/new', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  try {
    const members = await Member.getAllMembers();
    res.render('projects/new', {
      title: 'Tạo Dự án Mới',
      members,
      error: null,
      formData: {}
    });
  } catch (err) {
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Lỗi tải biểu mẫu.' });
  }
});

// Xử lý tạo mới dự án (POST)
router.post('/', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const { code, name, description, status, priority, start_date, end_date, budget, manager_id } = req.body;

  if (!code || !name) {
    const members = await Member.getAllMembers();
    return res.status(400).render('projects/new', {
      title: 'Tạo Dự án Mới',
      members,
      error: 'Mã dự án và Tên dự án là bắt buộc.',
      formData: req.body
    });
  }

  try {
    const created = await Project.createProject({
      code: code.trim().toUpperCase(),
      name: name.trim(),
      description: description ? description.trim() : '',
      status: status || 'Planning',
      priority: priority || 'Medium',
      start_date: start_date || new Date(),
      end_date: end_date || null,
      budget: budget ? parseFloat(budget) : 0,
      manager_id: manager_id ? parseInt(manager_id, 10) : null
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'CREATE_PROJECT',
      entityType: 'PROJECT',
      entityId: created.id,
      details: { code: created.code, name: created.name },
      ip: req.ip
    });

    res.redirect(`/projects/${created.id}`);
  } catch (err) {
    logger.error('create_project_error', 'Failed to create project', { error: err.message, body: req.body });
    const members = await Member.getAllMembers();
    res.status(500).render('projects/new', {
      title: 'Tạo Dự án Mới',
      members,
      error: 'Không thể tạo dự án: ' + (err.code === '23505' ? 'Mã dự án đã tồn tại.' : err.message),
      formData: req.body
    });
  }
});

// Chi tiết dự án
router.get('/:id', isAuthenticated, async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  try {
    const project = await Project.getProjectById(projectId);
    if (!project) {
      return res.status(404).render('error', { title: '404 Không tìm thấy', statusCode: 404, message: 'Dự án không tồn tại.' });
    }

    const tasks = await Task.getTasksByProject(projectId);
    const assignedMembers = await Member.getMembersForProject(projectId);
    const allMembers = await Member.getAllMembers();

    res.render('projects/detail', {
      title: `Chi tiết: ${project.name}`,
      project,
      tasks,
      assignedMembers,
      allMembers
    });
  } catch (err) {
    logger.error('project_detail_error', 'Failed to fetch project detail', { error: err.message, projectId });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể tải chi tiết dự án.' });
  }
});

// Chỉnh sửa dự án
router.get('/:id/edit', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  try {
    const project = await Project.getProjectById(projectId);
    if (!project) {
      return res.status(404).render('error', { title: '404', statusCode: 404, message: 'Dự án không tồn tại.' });
    }
    const members = await Member.getAllMembers();
    res.render('projects/edit', {
      title: `Chỉnh sửa Dự án: ${project.code}`,
      project,
      members,
      error: null
    });
  } catch (err) {
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể tải biểu mẫu chỉnh sửa.' });
  }
});

// Xử lý cập nhật dự án (POST)
router.post('/:id/edit', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  const { code, name, description, status, priority, start_date, end_date, budget, manager_id } = req.body;

  try {
    const updated = await Project.updateProject(projectId, {
      code: code.trim().toUpperCase(),
      name: name.trim(),
      description: description ? description.trim() : '',
      status,
      priority,
      start_date,
      end_date: end_date || null,
      budget: budget ? parseFloat(budget) : 0,
      manager_id: manager_id ? parseInt(manager_id, 10) : null
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'UPDATE_PROJECT',
      entityType: 'PROJECT',
      entityId: projectId,
      details: { code: updated.code, name: updated.name, status: updated.status },
      ip: req.ip
    });

    res.redirect(`/projects/${projectId}`);
  } catch (err) {
    logger.error('update_project_error', 'Failed to update project', { error: err.message, projectId });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể cập nhật dự án: ' + err.message });
  }
});

// Xóa dự án (POST)
router.post('/:id/delete', isAuthenticated, requireRole('admin'), async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  try {
    const deleted = await Project.deleteProject(projectId);
    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'DELETE_PROJECT',
      entityType: 'PROJECT',
      entityId: projectId,
      details: { name: deleted?.name },
      ip: req.ip
    });
    res.redirect('/projects');
  } catch (err) {
    logger.error('delete_project_error', 'Failed to delete project', { error: err.message, projectId });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể xóa dự án: ' + err.message });
  }
});

// Gán thành viên vào dự án
router.post('/:id/members', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  const { member_id, project_role } = req.body;

  try {
    await Member.assignMember(projectId, parseInt(member_id, 10), project_role || 'Member');
    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'ASSIGN_PROJECT_MEMBER',
      entityType: 'PROJECT_MEMBER',
      entityId: `${projectId}-${member_id}`,
      details: { projectId, memberId: member_id, role: project_role },
      ip: req.ip
    });
    res.redirect(`/projects/${projectId}`);
  } catch (err) {
    logger.error('assign_member_error', 'Failed to assign member to project', { error: err.message });
    res.redirect(`/projects/${projectId}?error=assign_failed`);
  }
});

// Xóa thành viên khỏi dự án
router.post('/:id/members/:memberId/remove', isAuthenticated, requireRole('admin', 'manager'), async (req, res) => {
  const projectId = parseInt(req.params.id, 10);
  const memberId = parseInt(req.params.memberId, 10);

  try {
    await Member.removeMember(projectId, memberId);
    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'REMOVE_PROJECT_MEMBER',
      entityType: 'PROJECT_MEMBER',
      entityId: `${projectId}-${memberId}`,
      details: { projectId, memberId },
      ip: req.ip
    });
    res.redirect(`/projects/${projectId}`);
  } catch (err) {
    logger.error('remove_member_error', 'Failed to remove member from project', { error: err.message });
    res.redirect(`/projects/${projectId}`);
  }
});

module.exports = router;
