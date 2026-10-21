const db = require('../config/db');
const bcrypt = require('bcryptjs');

async function findByUsername(username) {
  const res = await db.query('SELECT * FROM users WHERE username = $1', [username]);
  return res.rows[0] || null;
}

async function findById(id) {
  const res = await db.query('SELECT id, username, email, role, created_at FROM users WHERE id = $1', [id]);
  return res.rows[0] || null;
}

async function verifyPassword(plainPassword, passwordHash) {
  return bcrypt.compare(plainPassword, passwordHash);
}

async function createUser(username, email, plainPassword, role = 'user') {
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(plainPassword, salt);
  const res = await db.query(
    'INSERT INTO users (username, email, password_hash, role) VALUES ($1, $2, $3, $4) RETURNING id, username, email, role',
    [username, email, hash, role]
  );
  return res.rows[0];
}

module.exports = {
  findByUsername,
  findById,
  verifyPassword,
  createUser
};
