import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import BottomNav from './BottomNav';

const Layout = () => {
  const location = useLocation();
  const isAuthPage = ['/login', '/register', '/admin/login'].includes(location.pathname);

  return (
    <div style={{ paddingBottom: isAuthPage ? 0 : '80px', minHeight: '100vh' }}>
      <Outlet />
      {!isAuthPage && <BottomNav />}
    </div>
  );
};

export default Layout;
