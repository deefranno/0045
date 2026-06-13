const cron = require('node-cron');
const db = require('../db/database');
const wipay = require('../gateways/wipay');
const { sendEmail, adminWeeklyReport } = require('../email/templates');

const startJobs = () => {
  if (process.env.ENABLE_JOBS !== 'true' && process.env.NODE_ENV !== 'production') {
    return;
  }

  // Daily 9:00 AM — WiPay renewals
  cron.schedule('0 9 * * *', async () => {
    await wipay.handleRecurring();
  });

  // Daily midnight — Mark overdue invoices
  cron.schedule('0 0 * * *', () => {
    db.prepare(`
      UPDATE invoices
      SET status = 'overdue'
      WHERE due_date < date('now')
      AND status = 'pending'
    `).run();
    console.log('Cron: Marked overdue invoices');
  });

  // Daily 1:00 AM — Past due subscriptions
  cron.schedule('0 1 * * *', () => {
    db.prepare(`
      UPDATE subscriptions
      SET status = 'past_due'
      WHERE current_period_end < CURRENT_TIMESTAMP
      AND status = 'active'
    `).run();
    console.log('Cron: Checked subscription statuses');
  });

  // Sunday 8:00 AM — Admin report
  cron.schedule('0 8 * * 0', async () => {
    const total_users = db.prepare('SELECT COUNT(*) as count FROM users').get().count;
    const active_subs = db.prepare("SELECT COUNT(*) as count FROM subscriptions WHERE status = 'active'").get().count;

    await sendEmail(process.env.ADMIN_EMAIL, adminWeeklyReport({
      total_users,
      active_subs,
      generated_at: new Date().toISOString()
    }));
  });
};

module.exports = startJobs;
