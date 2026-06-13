import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import AnnouncementBanner from '../components/AnnouncementBanner';
import { Plus, Users, FileText, BarChart3, ChevronRight } from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/dashboard/summary');
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;

  const getTimeOfDay = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'morning';
    if (hour < 18) return 'afternoon';
    return 'evening';
  };

  const flags = { JA: '🇯🇲', TT: '🇹🇹', BB: '🇧🇧', GY: '🇬🇾', other: '🌍' };

  return (
    <div style={{ padding: '16px' }}>
      {/* Top Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '28px', height: '28px', background: 'var(--brand)', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold' }}>Q</div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 'bold', lineHeight: 1 }}>QuickInvoice</div>
            <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Caribbean</div>
          </div>
        </div>
        <div style={{ width: '36px', height: '36px', background: 'var(--brand)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: '600' }}>
          {user?.name?.[0]}
        </div>
      </div>

      <AnnouncementBanner />

      {/* Hero Card */}
      <div className="hero-card" style={{ marginBottom: '20px' }}>
        <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '4px' }}>Good {getTimeOfDay()}, {user?.name.split(' ')[0]}</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '16px' }}>
          <div>
            <div style={{ fontSize: '12px', opacity: 0.8 }}>Outstanding Balance</div>
            <div style={{ fontSize: '32px', fontWeight: '700' }}>
              ${data?.total_outstanding?.toLocaleString() || '0'}
            </div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.2)', padding: '4px 10px', borderRadius: '12px', fontSize: '12px', fontWeight: '600' }}>
            {user?.default_currency || 'JMD'}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '20px', borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: '12px' }}>
          <div>
            <div style={{ fontSize: '10px', opacity: 0.8 }}>Active Invoices</div>
            <div style={{ fontSize: '16px', fontWeight: '600' }}>{data?.active_invoice_count}</div>
          </div>
          <div style={{ width: '1px', background: 'rgba(255,255,255,0.2)' }}></div>
          <div>
            <div style={{ fontSize: '10px', opacity: 0.8 }}>Overdue</div>
            <div style={{ fontSize: '16px', fontWeight: '600' }}>{data?.overdue_count}</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ display: 'flex', gap: '12px', overflowX: 'auto', paddingBottom: '8px', marginBottom: '20px', scrollbarWidth: 'none' }}>
        <QuickAction to="/invoices/new" icon={<Plus size={20} />} label="New Invoice" />
        <QuickAction to="/clients" icon={<Users size={20} />} label="Clients" />
        <QuickAction to="/reports" icon={<BarChart3 size={20} />} label="Reports" />
      </div>

      {/* Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '24px' }}>
        <div className="card" style={{ padding: '12px' }}>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Paid This Month</div>
          <div style={{ fontSize: '18px', fontWeight: '700', color: 'var(--brand)' }}>${data?.paid_this_month?.toLocaleString()}</div>
        </div>
        <div className="card" style={{ padding: '12px' }}>
          <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Overdue</div>
          <div style={{ fontSize: '18px', fontWeight: '700', color: 'var(--danger)' }}>${data?.overdue_amount?.toLocaleString()}</div>
        </div>
      </div>

      {/* Recent Invoices */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <h2 style={{ fontSize: '16px', margin: 0 }}>Recent Invoices</h2>
          <Link to="/invoices" style={{ fontSize: '13px', color: 'var(--brand)', textDecoration: 'none', fontWeight: '600' }}>See all</Link>
        </div>
        {data?.recent_invoices.map(inv => (
          <Link key={inv.id} to={`/invoices/${inv.id}`} className="card" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none', color: 'inherit', marginBottom: '8px' }}>
            <div style={{ width: '40px', height: '40px', background: 'var(--brand-light)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>
              {flags[inv.client_country] || '🌍'}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '14px', fontWeight: '600' }}>{inv.client_name}</div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{inv.invoice_number}</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '14px', fontWeight: '700' }}>${inv.total.toLocaleString()}</div>
              <div className={`badge badge-${inv.status}`}>{inv.status}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

const QuickAction = ({ to, icon, label }) => (
  <Link to={to} style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '8px',
    minWidth: '80px',
    textDecoration: 'none',
    color: 'inherit'
  }}>
    <div style={{ width: '48px', height: '48px', background: 'white', borderRadius: '14px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--brand)', boxShadow: 'var(--shadow)' }}>
      {icon}
    </div>
    <span style={{ fontSize: '11px', fontWeight: '500' }}>{label}</span>
  </Link>
);

export default Dashboard;
