const db = require('../config/db');

async function getAllProjects(filters = {}) {
  let query = `
    SELECT p.*, m.full_name AS manager_name,
           COUNT(DISTINCT t.id) AS total_tasks,
           COUNT(DISTINCT CASE WHEN t.status = 'Done' THEN t.id END) AS completed_tasks,
           COUNT(DISTINCT pm.member_id) AS total_members
    FROM projects p
    LEFT JOIN members m ON p.manager_id = m.id
    LEFT JOIN tasks t ON p.id = t.project_id
    LEFT JOIN project_members pm ON p.id = pm.project_id
  `;
  const params = [];
  const conditions = [];

  if (filters.status) {
    params.push(filters.status);
    conditions.push(`p.status = $${params.length}`);
  }
  if (filters.priority) {
    params.push(filters.priority);
    conditions.push(`p.priority = $${params.length}`);
  }
  if (filters.search) {
    params.push(`%${filters.search}%`);
    conditions.push(`(p.name ILIKE $${params.length} OR p.code ILIKE $${params.length})`);
  }

  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }

  query += ' GROUP BY p.id, m.full_name ORDER BY p.id ASC';

  const res = await db.query(query, params);
  return res.rows;
}

async function getProjectById(id) {
  const query = `
    SELECT p.*, m.full_name AS manager_name, m.email AS manager_email,
           COUNT(DISTINCT t.id) AS total_tasks,
           COUNT(DISTINCT CASE WHEN t.status = 'Done' THEN t.id END) AS completed_tasks
    FROM projects p
    LEFT JOIN members m ON p.manager_id = m.id
    LEFT JOIN tasks t ON p.id = t.project_id
    WHERE p.id = $1
    GROUP BY p.id, m.full_name, m.email
  `;
  const res = await db.query(query, [id]);
  return res.rows[0] || null;
}

async function createProject({ code, name, description, status = 'Planning', priority = 'Medium', start_date, end_date, budget = 0, manager_id = null }) {
  const res = await db.query(
    `INSERT INTO projects (code, name, description, status, priority, start_date, end_date, budget, manager_id)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
     RETURNING *`,
    [code, name, description, status, priority, start_date || new Date(), end_date || null, budget, manager_id]
  );
  return res.rows[0];
}

async function updateProject(id, { code, name, description, status, priority, start_date, end_date, budget, manager_id }) {
  const res = await db.query(
    `UPDATE projects
     SET code = $1, name = $2, description = $3, status = $4, priority = $5,
         start_date = $6, end_date = $7, budget = $8, manager_id = $9, updated_at = CURRENT_TIMESTAMP
     WHERE id = $10
     RETURNING *`,
    [code, name, description, status, priority, start_date, end_date || null, budget, manager_id, id]
  );
  return res.rows[0];
}

async function deleteProject(id) {
  const res = await db.query('DELETE FROM projects WHERE id = $1 RETURNING id, name', [id]);
  return res.rows[0];
}

async function getDashboardStats() {
  const projectStats = await db.query(`
    SELECT 
      COUNT(*) AS total_projects,
      COUNT(CASE WHEN status = 'In Progress' THEN 1 END) AS in_progress_projects,
      COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed_projects,
      COUNT(CASE WHEN status = 'Planning' THEN 1 END) AS planning_projects
    FROM projects
  `);

  const taskStats = await db.query(`
    SELECT 
      COUNT(*) AS total_tasks,
      COUNT(CASE WHEN status = 'Todo' THEN 1 END) AS todo_tasks,
      COUNT(CASE WHEN status = 'In Progress' THEN 1 END) AS in_progress_tasks,
      COUNT(CASE WHEN status = 'Done' THEN 1 END) AS done_tasks,
      COUNT(CASE WHEN due_date < CURRENT_DATE AND status != 'Done' THEN 1 END) AS overdue_tasks
    FROM tasks
  `);

  const memberStats = await db.query(`
    SELECT COUNT(*) AS total_members,
           COUNT(CASE WHEN status = 'Active' THEN 1 END) AS active_members
    FROM members
  `);

  return {
    projects: projectStats.rows[0],
    tasks: taskStats.rows[0],
    members: memberStats.rows[0]
  };
}

module.exports = {
  getAllProjects,
  getProjectById,
  createProject,
  updateProject,
  deleteProject,
  getDashboardStats
};
