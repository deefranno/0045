const crypto = require('crypto');

module.exports = {
  createPaymentLink: async (params) => {
    const { amount, currency, order_id } = params;
    const merchant_id = process.env.EZEE_MERCHANT_ID;
    const secret_key = process.env.EZEE_SECRET_KEY;

    const data = `${merchant_id}${amount}${currency}${order_id}`;
    const signature = crypto.createHmac('sha256', secret_key).update(data).digest('hex');

    const payment_url = `https://ezeepayments.com/checkout?m=${merchant_id}&a=${amount}&c=${currency}&o=${order_id}&s=${signature}`;

    return { payment_url };
  }
};
