const db = require('../config/db');
const logger = require('../config/logger');

async function logAction({ userId = null, username = 'anonymous', action, entityType = null, entityId = null, details = {}, ip = '127.0.0.1' }) {
  try {
    await db.query(
      `INSERT INTO audit_logs (user_id, username, action, entity_type, entity_id, details, ip_address)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [userId, username, action, entityType, entityId ? String(entityId) : null, JSON.stringify(details), ip]
    );

    logger.audit(action, `Audit event recorded: ${action}`, {
      user: username,
      userId,
      entityType,
      entityId,
      details,
      ip
    });
  } catch (err) {
    logger.error('audit_log_error', 'Failed to insert audit log entry into database', {
      error: err.message,
      action
    });
  }
}

async function getRecentLogs(limit = 50) {
  const res = await db.query(
    'SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT $1',
    [limit]
  );
  return res.rows;
}

module.exports = {
  logAction,
  getRecentLogs
};
