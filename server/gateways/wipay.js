const axios = require('axios');
const db = require('../db/database');

const BASE_URL = process.env.WIPAY_ENVIRONMENT === 'live'
  ? 'https://wipayfinancial.com/v1/api'
  : 'https://sandbox.wipayfinancial.com/v1/api';

module.exports = {
  createPaymentLink: async (params) => {
    const { amount, currency, order_id } = params;

    const url = `${BASE_URL}/payment?account_number=${process.env.WIPAY_ACCOUNT_NUMBER}&total=${amount}&currency=${currency}&order_id=${order_id}`;

    return { payment_url: url };
  },

  verifyTransaction: async (transaction_id) => {
    const res = await axios.get(`${BASE_URL}/verify?transaction_id=${transaction_id}`);
    return res.data;
  },

  handleRecurring: async () => {
    const today = new Date().toISOString().split('T')[0];
    const dueSubs = db.prepare("SELECT * FROM subscriptions WHERE payment_gateway = 'wipay' AND current_period_end = ? AND status = 'active'").all(today);

    for (const sub of dueSubs) {
      console.log(`Sending WiPay renewal email to user ${sub.user_id}`);
    }
  }
};
