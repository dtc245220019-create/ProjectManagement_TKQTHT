const express = require('express');
const router = express.Router();
const Task = require('../models/task');
const Project = require('../models/project');
const Member = require('../models/member');
const Audit = require('../models/audit');
const { isAuthenticated, requireRole } = require('../middleware/auth');
const logger = require('../config/logger');

// Danh sách toàn bộ công việc
router.get('/', isAuthenticated, async (req, res) => {
  try {
    const { status, priority, projectId, assignedTo } = req.query;
    const tasks = await Task.getAllTasks({ status, priority, projectId, assignedTo });
    const projects = await Project.getAllProjects();
    const members = await Member.getAllMembers();

    res.render('tasks/list', {
      title: 'Quản lý Công việc (Tasks)',
      tasks,
      projects,
      members,
      filters: { status, priority, projectId, assignedTo }
    });
  } catch (err) {
    logger.error('tasks_fetch_error', 'Failed to fetch tasks', { error: err.message });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Không thể tải danh sách công việc.' });
  }
});

// Trang tạo mới task
router.get('/new', isAuthenticated, async (req, res) => {
  const projectId = req.query.projectId ? parseInt(req.query.projectId, 10) : null;
  try {
    const projects = await Project.getAllProjects();
    const members = projectId ? await Member.getMembersForProject(projectId) : await Member.getAllMembers();

    res.render('tasks/new', {
      title: 'Tạo Công việc Mới',
      projects,
      members,
      selectedProjectId: projectId,
      error: null,
      formData: {}
    });
  } catch (err) {
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Lỗi tải biểu mẫu.' });
  }
});

// Xử lý tạo mới task (POST)
router.post('/', isAuthenticated, async (req, res) => {
  const { project_id, title, description, status, priority, assigned_to, due_date, estimated_hours } = req.body;

  if (!project_id || !title) {
    const projects = await Project.getAllProjects();
    const members = await Member.getAllMembers();
    return res.status(400).render('tasks/new', {
      title: 'Tạo Công việc Mới',
      projects,
      members,
      selectedProjectId: project_id,
      error: 'Vui lòng chọn Dự án và nhập Tiêu đề công việc.',
      formData: req.body
    });
  }

  try {
    const created = await Task.createTask({
      project_id: parseInt(project_id, 10),
      title: title.trim(),
      description: description ? description.trim() : '',
      status: status || 'Todo',
      priority: priority || 'Medium',
      assigned_to: assigned_to ? parseInt(assigned_to, 10) : null,
      due_date: due_date || null,
      estimated_hours: estimated_hours ? parseFloat(estimated_hours) : 0
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'CREATE_TASK',
      entityType: 'TASK',
      entityId: created.id,
      details: { title: created.title, projectId: created.project_id },
      ip: req.ip
    });

    res.redirect(`/projects/${created.project_id}`);
  } catch (err) {
    logger.error('create_task_error', 'Failed to create task', { error: err.message });
    const projects = await Project.getAllProjects();
    const members = await Member.getAllMembers();
    res.status(500).render('tasks/new', {
      title: 'Tạo Công việc Mới',
      projects,
      members,
      selectedProjectId: project_id,
      error: 'Không thể tạo task: ' + err.message,
      formData: req.body
    });
  }
});

// Cập nhật trạng thái nhanh của task (POST)
router.post('/:id/status', isAuthenticated, async (req, res) => {
  const taskId = parseInt(req.params.id, 10);
  const { status, redirect } = req.body;

  try {
    const task = await Task.getTaskById(taskId);
    if (!task) {
      return res.status(404).send('Task not found');
    }

    await Task.updateTask(taskId, {
      title: task.title,
      description: task.description,
      status: status || task.status,
      priority: task.priority,
      assigned_to: task.assigned_to,
      due_date: task.due_date,
      estimated_hours: task.estimated_hours,
      actual_hours: task.actual_hours
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'UPDATE_TASK_STATUS',
      entityType: 'TASK',
      entityId: taskId,
      details: { oldStatus: task.status, newStatus: status },
      ip: req.ip
    });

    res.redirect(redirect || `/projects/${task.project_id}`);
  } catch (err) {
    logger.error('update_task_status_error', 'Failed to update task status', { error: err.message, taskId });
    res.redirect(redirect || '/tasks');
  }
});

// Chỉnh sửa đầy đủ task (POST)
router.post('/:id/edit', isAuthenticated, async (req, res) => {
  const taskId = parseInt(req.params.id, 10);
  const { title, description, status, priority, assigned_to, due_date, estimated_hours, actual_hours, redirect } = req.body;

  try {
    const updated = await Task.updateTask(taskId, {
      title: title.trim(),
      description: description ? description.trim() : '',
      status,
      priority,
      assigned_to: assigned_to ? parseInt(assigned_to, 10) : null,
      due_date: due_date || null,
      estimated_hours: estimated_hours ? parseFloat(estimated_hours) : 0,
      actual_hours: actual_hours ? parseFloat(actual_hours) : 0
    });

    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'UPDATE_TASK',
      entityType: 'TASK',
      entityId: taskId,
      details: { title: updated.title, status: updated.status },
      ip: req.ip
    });

    res.redirect(redirect || `/projects/${updated.project_id}`);
  } catch (err) {
    logger.error('update_task_error', 'Failed to update task', { error: err.message, taskId });
    res.redirect(redirect || '/tasks');
  }
});

// Xóa task (POST)
router.post('/:id/delete', isAuthenticated, async (req, res) => {
  const taskId = parseInt(req.params.id, 10);
  const { redirect } = req.body;

  try {
    const deleted = await Task.deleteTask(taskId);
    await Audit.logAction({
      userId: req.session.user.id,
      username: req.session.user.username,
      action: 'DELETE_TASK',
      entityType: 'TASK',
      entityId: taskId,
      details: { title: deleted?.title },
      ip: req.ip
    });
    res.redirect(redirect || `/projects/${deleted.project_id}`);
  } catch (err) {
    logger.error('delete_task_error', 'Failed to delete task', { error: err.message, taskId });
    res.redirect(redirect || '/tasks');
  }
});

module.exports = router;
