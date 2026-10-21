const express = require('express');
const router = express.Router();
const Project = require('../models/project');
const Task = require('../models/task');
const Member = require('../models/member');
const Audit = require('../models/audit');
const db = require('../config/db');
const { isAuthenticated } = require('../middleware/auth');
const logger = require('../config/logger');

// Health Check Endpoint
router.get('/health', async (req, res) => {
  const dbHealth = await db.checkHealth();
  const isHealthy = dbHealth.status === 'CONNECTED';
  const statusCode = isHealthy ? 200 : 503;

  const response = {
    status: isHealthy ? 'UP' : 'DOWN',
    timestamp: new Date().toISOString(),
    service: 'project-management-app',
    version: '1.0.0',
    uptime_seconds: Math.floor(process.uptime()),
    database: dbHealth,
    memory: {
      rss_mb: (process.memoryUsage().rss / 1024 / 1024).toFixed(2),
      heap_used_mb: (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2)
    }
  };

  res.status(statusCode).json(response);
});

// Dashboard chính
router.get('/', isAuthenticated, async (req, res) => {
  try {
    const stats = await Project.getDashboardStats();
    const recentProjects = await Project.getAllProjects();
    const recentTasks = await Task.getAllTasks();
    const recentAudits = await Audit.getRecentLogs(10);

    res.render('dashboard', {
      title: 'Bảng Điều khiển Dự án - Project Management System',
      stats,
      projects: recentProjects.slice(0, 5),
      tasks: recentTasks.slice(0, 8),
      audits: recentAudits
    });
  } catch (err) {
    logger.error('dashboard_error', 'Failed to render dashboard', { error: err.message });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Lỗi tải trang tổng quan.' });
  }
});

// Nhật ký kiểm toán (Audit Logs)
router.get('/audit', isAuthenticated, async (req, res) => {
  try {
    const logs = await Audit.getRecentLogs(100);
    res.render('audit/list', {
      title: 'Nhật ký Hoạt động & Kiểm toán (Audit Logs)',
      logs
    });
  } catch (err) {
    logger.error('audit_fetch_error', 'Failed to fetch audit logs', { error: err.message });
    res.status(500).render('error', { title: 'Lỗi', statusCode: 500, message: 'Lỗi tải nhật ký kiểm toán.' });
  }
});

module.exports = router;
