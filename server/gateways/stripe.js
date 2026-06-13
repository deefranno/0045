const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

module.exports = {
  createCheckoutSession: async (user, plan, billing_cycle) => {
    let customerId = user.gateway_customer_id;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        name: user.name,
        metadata: { userId: user.id }
      });
      customerId = customer.id;
    }

    const priceId = process.env[`STRIPE_${plan.toUpperCase()}_${billing_cycle.toUpperCase()}_PRICE_ID`];

    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      success_url: `${process.env.APP_URL}/subscription/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.APP_URL}/pricing`,
    });

    return { payment_url: session.url };
  },

  handleWebhook: async (payload, signature) => {
    const event = stripe.webhooks.constructEvent(payload, signature, process.env.STRIPE_WEBHOOK_SECRET);
    return event;
  },

  cancelSubscription: async (subscriptionId) => {
    return await stripe.subscriptions.update(subscriptionId, { cancel_at_period_end: true });
  }
};
