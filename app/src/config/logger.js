const fs = require('fs');
const path = require('path');

const logDir = process.env.LOG_DIR || path.join(__dirname, '../../logs');
if (!fs.existsSync(logDir)) {
  try {
    fs.mkdirSync(logDir, { recursive: true });
  } catch (err) {
    console.error('Cannot create log directory:', err.message);
  }
}

const logFile = path.join(logDir, 'app.log');

function writeLog(level, event, message, meta = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    event,
    message,
    service: 'project-management-app',
    ...meta
  };

  const line = JSON.stringify(entry) + '\n';

  // Output to stdout for Docker log collectors
  if (level === 'error') {
    process.stderr.write(line);
  } else {
    process.stdout.write(line);
  }

  // Append to named volume log file for Promtail
  try {
    fs.appendFileSync(logFile, line, { encoding: 'utf8' });
  } catch (err) {
    // Volume might not be ready or writable, ignore to prevent app crash
  }
}

const logger = {
  info: (event, message, meta) => writeLog('info', event, message, meta),
  warn: (event, message, meta) => writeLog('warn', event, message, meta),
  error: (event, message, meta) => writeLog('error', event, message, meta),
  audit: (event, message, meta) => writeLog('info', 'audit', message, { audit_event: event, ...meta })
};

module.exports = logger;
