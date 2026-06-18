const Database = require('better-sqlite3');
const path = require('path');

const dbPath = process.env.NODE_ENV === 'production'
  ? '/tmp/quickinvoice.sqlite'
  : path.join(__dirname, 'quickinvoice.sqlite');

const db = new Database(dbPath);
db.pragma('journal_mode = WAL');

module.exports = db;
