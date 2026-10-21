const db = require('../config/db');

async function getTasksByProject(projectId) {
  const query = `
    SELECT t.*, m.full_name AS assignee_name, m.email AS assignee_email
    FROM tasks t
    LEFT JOIN members m ON t.assigned_to = m.id
    WHERE t.project_id = $1
    ORDER BY 
      CASE t.status
        WHEN 'In Progress' THEN 1
        WHEN 'Todo' THEN 2
        WHEN 'Review' THEN 3
        WHEN 'Done' THEN 4
        ELSE 5
      END,
      t.due_date ASC NULLS LAST
  `;
  const res = await db.query(query, [projectId]);
  return res.rows;
}

async function getAllTasks(filters = {}) {
  let query = `
    SELECT t.*, p.name AS project_name, p.code AS project_code,
           m.full_name AS assignee_name
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    LEFT JOIN members m ON t.assigned_to = m.id
  `;
  const params = [];
  const conditions = [];

  if (filters.status) {
    params.push(filters.status);
    conditions.push(`t.status = $${params.length}`);
  }
  if (filters.priority) {
    params.push(filters.priority);
    conditions.push(`t.priority = $${params.length}`);
  }
  if (filters.projectId) {
    params.push(filters.projectId);
    conditions.push(`t.project_id = $${params.length}`);
  }
  if (filters.assignedTo) {
    params.push(filters.assignedTo);
    conditions.push(`t.assigned_to = $${params.length}`);
  }

  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }

  query += ' ORDER BY t.id DESC LIMIT 100';

  const res = await db.query(query, params);
  return res.rows;
}

async function getTaskById(id) {
  const query = `
    SELECT t.*, p.name AS project_name, p.code AS project_code,
           m.full_name AS assignee_name
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    LEFT JOIN members m ON t.assigned_to = m.id
    WHERE t.id = $1
  `;
  const res = await db.query(query, [id]);
  return res.rows[0] || null;
}

async function createTask({ project_id, title, description, status = 'Todo', priority = 'Medium', assigned_to = null, due_date = null, estimated_hours = 0 }) {
  const res = await db.query(
    `INSERT INTO tasks (project_id, title, description, status, priority, assigned_to, due_date, estimated_hours)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
     RETURNING *`,
    [project_id, title, description, status, priority, assigned_to, due_date || null, estimated_hours]
  );
  return res.rows[0];
}

async function updateTask(id, { title, description, status, priority, assigned_to, due_date, estimated_hours, actual_hours }) {
  const res = await db.query(
    `UPDATE tasks
     SET title = $1, description = $2, status = $3, priority = $4,
         assigned_to = $5, due_date = $6, estimated_hours = $7, actual_hours = $8, updated_at = CURRENT_TIMESTAMP
     WHERE id = $9
     RETURNING *`,
    [title, description, status, priority, assigned_to || null, due_date || null, estimated_hours, actual_hours, id]
  );
  return res.rows[0];
}

async function deleteTask(id) {
  const res = await db.query('DELETE FROM tasks WHERE id = $1 RETURNING id, title, project_id', [id]);
  return res.rows[0];
}

module.exports = {
  getTasksByProject,
  getAllTasks,
  getTaskById,
  createTask,
  updateTask,
  deleteTask
};
