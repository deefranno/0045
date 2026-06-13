import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const AdminSubscriptions = () => {
  const [subs, setSubs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubs();
  }, []);

  const fetchSubs = async () => {
    try {
      const res = await api.get('/admin/users', {
        headers: { Authorization: `Bearer ${localStorage.getItem('qi_admin_token')}` }
      });
      setSubs(res.data);
    } catch (err) {} finally { setLoading(false); }
  };

  return (
    <div>
      <h1 style={{ fontSize: '24px', marginBottom: '32px' }}>Subscriptions</h1>
      <div className="card" style={{ padding: 0 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ background: '#F9FAFB' }}>
            <tr style={{ textAlign: 'left', fontSize: '12px', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '16px' }}>User</th>
              <th>Plan</th>
              <th>Status</th>
              <th>Gateway</th>
              <th>Cycle</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {subs.map(u => (
              <tr key={u.id} style={{ borderTop: '1px solid var(--border)', fontSize: '14px' }}>
                <td style={{ padding: '16px' }}>
                  <div style={{ fontWeight: '600' }}>{u.name}</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{u.email}</div>
                </td>
                <td><span className="badge" style={{ background: '#E8F7F2', color: '#0F6E56' }}>{u.plan.toUpperCase()}</span></td>
                <td><span style={{ fontSize: '12px', fontWeight: '600', color: u.subscription_status === 'active' ? 'var(--brand)' : 'var(--danger)' }}>{u.subscription_status || 'N/A'}</span></td>
                <td>Stripe</td>
                <td>Monthly</td>
                <td>
                  <button style={{ color: 'var(--brand)', background: 'none', border: 'none', fontWeight: '600', cursor: 'pointer' }}>Cancel</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminSubscriptions;
