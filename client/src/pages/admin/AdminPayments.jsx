import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const AdminPayments = () => {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPayments();
  }, []);

  const fetchPayments = async () => {
    try {
      const res = await api.get('/admin/stats', {
        headers: { Authorization: `Bearer ${localStorage.getItem('qi_admin_token')}` }
      });
      setPayments(res.data.recent_payments);
    } catch (err) {} finally { setLoading(false); }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <h1 style={{ fontSize: '24px', margin: 0 }}>Payments</h1>
        <button className="btn-ghost" style={{ width: 'auto', padding: '8px 16px' }}>Export CSV</button>
      </div>

      <div className="card" style={{ padding: 0 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ background: '#F9FAFB' }}>
            <tr style={{ textAlign: 'left', fontSize: '12px', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '16px' }}>Date</th>
              <th>Amount</th>
              <th>Gateway</th>
              <th>Status</th>
              <th>Transaction ID</th>
            </tr>
          </thead>
          <tbody>
            {payments.map(p => (
              <tr key={p.id} style={{ borderTop: '1px solid var(--border)', fontSize: '14px' }}>
                <td style={{ padding: '16px' }}>{new Date(p.created_at).toLocaleDateString()}</td>
                <td><span style={{ fontWeight: '700' }}>{p.currency} ${p.amount}</span></td>
                <td><span className="badge" style={{ background: '#F2F7F5' }}>{p.payment_gateway.toUpperCase()}</span></td>
                <td><span className="badge badge-paid">{p.status}</span></td>
                <td style={{ fontSize: '12px', color: 'var(--text-hint)' }}>{p.gateway_payment_id || '---'}</td>
              </tr>
            ))}
            {payments.length === 0 && (
              <tr><td colSpan="5" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>No payments found</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminPayments;
