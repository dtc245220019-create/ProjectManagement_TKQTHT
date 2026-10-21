const db = require('../config/db');

async function getAllMembers() {
  const query = `
    SELECT m.*, u.username 
    FROM members m
    LEFT JOIN users u ON m.user_id = u.id
    ORDER BY m.id ASC
  `;
  const res = await db.query(query);
  return res.rows;
}

async function getMemberById(id) {
  const res = await db.query('SELECT * FROM members WHERE id = $1', [id]);
  return res.rows[0] || null;
}

async function createMember({ full_name, email, role, department, phone, status = 'Active', user_id = null }) {
  const res = await db.query(
    `INSERT INTO members (full_name, email, role, department, phone, status, user_id)
     VALUES ($1, $2, $3, $4, $5, $6, $7)
     RETURNING *`,
    [full_name, email, role, department, phone, status, user_id]
  );
  return res.rows[0];
}

async function updateMember(id, { full_name, email, role, department, phone, status }) {
  const res = await db.query(
    `UPDATE members 
     SET full_name = $1, email = $2, role = $3, department = $4, phone = $5, status = $6, updated_at = CURRENT_TIMESTAMP
     WHERE id = $7
     RETURNING *`,
    [full_name, email, role, department, phone, status, id]
  );
  return res.rows[0];
}

async function deleteMember(id) {
  const res = await db.query('DELETE FROM members WHERE id = $1 RETURNING id, full_name', [id]);
  return res.rows[0];
}

async function getMembersForProject(projectId) {
  const query = `
    SELECT m.id, m.full_name, m.email, m.department, pm.project_role, pm.joined_at
    FROM project_members pm
    JOIN members m ON pm.member_id = m.id
    WHERE pm.project_id = $1
    ORDER BY pm.joined_at ASC
  `;
  const res = await db.query(query, [projectId]);
  return res.rows;
}

async function assignMember(projectId, memberId, projectRole = 'Member') {
  const res = await db.query(
    `INSERT INTO project_members (project_id, member_id, project_role)
     VALUES ($1, $2, $3)
     ON CONFLICT (project_id, member_id) 
     DO UPDATE SET project_role = EXCLUDED.project_role
     RETURNING *`,
    [projectId, memberId, projectRole]
  );
  return res.rows[0];
}

async function removeMember(projectId, memberId) {
  const res = await db.query(
    'DELETE FROM project_members WHERE project_id = $1 AND member_id = $2 RETURNING *',
    [projectId, memberId]
  );
  return res.rows[0];
}

module.exports = {
  getAllMembers,
  getMemberById,
  createMember,
  updateMember,
  deleteMember,
  getMembersForProject,
  assignMember,
  removeMember
};
