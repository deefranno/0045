import React, { useState, useEffect } from 'react';
import api from '../../utils/api';

const AdminLogs = () => {
  const [logs, setLogs] = useState([]);

  return (
    <div>
      <h1 style={{ fontSize: '24px', marginBottom: '32px' }}>System Logs</h1>
      <div className="card" style={{ padding: 0 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ background: '#F9FAFB' }}>
            <tr style={{ textAlign: 'left', fontSize: '12px', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '16px' }}>Timestamp</th>
              <th>Admin</th>
              <th>Action</th>
              <th>Target</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan="5" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>No audit logs found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminLogs;
