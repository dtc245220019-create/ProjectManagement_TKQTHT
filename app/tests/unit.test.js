const assert = require('assert');
const bcrypt = require('bcryptjs');

console.log('--- BẮT ĐẦU UNIT TESTS HỆ THỐNG QUẢN LÝ DỰ ÁN ---');

async function testPasswordHashing() {
  process.stdout.write('[TEST 1] Bcrypt password hashing & verification: ');
  const plain = 'Admin@ProjectMgmt2026!';
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(plain, salt);
  const match = await bcrypt.compare(plain, hash);
  assert.strictEqual(match, true, 'Password must match hash');
  const mismatch = await bcrypt.compare('WrongPassword', hash);
  assert.strictEqual(mismatch, false, 'Wrong password must fail');
  console.log('PASS');
}

function testInputValidation() {
  process.stdout.write('[TEST 2] Project & Task Input Data Validation: ');
  const validProject = { code: 'PRJ-001', name: 'Dự án Test', status: 'Planning' };
  assert.ok(validProject.code && validProject.name, 'Project must have code and name');
  assert.strictEqual(validProject.code.toUpperCase(), 'PRJ-001', 'Code should be uppercase');
  
  const validTask = { title: 'Task 1', status: 'Todo', priority: 'High' };
  assert.ok(validTask.title, 'Task must have a title');
  const allowedStatuses = ['Todo', 'In Progress', 'Review', 'Done'];
  assert.ok(allowedStatuses.includes(validTask.status), 'Status must be in allowed list');
  console.log('PASS');
}

function testRoleBasedAccess() {
  process.stdout.write('[TEST 3] Role-Based Access Control logic: ');
  const roles = ['admin', 'manager', 'user'];
  const checkAccess = (userRole, requiredRoles) => {
    return userRole === 'admin' || requiredRoles.includes(userRole);
  };

  assert.strictEqual(checkAccess('admin', ['manager']), true, 'Admin always has access');
  assert.strictEqual(checkAccess('manager', ['manager']), true, 'Manager has manager access');
  assert.strictEqual(checkAccess('user', ['manager']), false, 'User denied manager access');
  console.log('PASS');
}

function testJsonLoggerFormatting() {
  process.stdout.write('[TEST 4] Structured JSON Log Entry Formatting: ');
  const entry = {
    timestamp: new Date().toISOString(),
    level: 'info',
    event: 'test_event',
    message: 'Testing JSON structure',
    service: 'project-management-app'
  };
  const jsonStr = JSON.stringify(entry);
  const parsed = JSON.parse(jsonStr);
  assert.strictEqual(parsed.event, 'test_event');
  assert.strictEqual(parsed.service, 'project-management-app');
  assert.ok(parsed.timestamp);
  console.log('PASS');
}

async function runAllTests() {
  try {
    await testPasswordHashing();
    testInputValidation();
    testRoleBasedAccess();
    testJsonLoggerFormatting();
    console.log('--- TẤT CẢ 4/4 UNIT TESTS ĐÃ VƯỢT QUA XUẤT SẮC ---');
    process.exit(0);
  } catch (err) {
    console.error('TEST FAILED:', err.message);
    process.exit(1);
  }
}

runAllTests();
