import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import SupplierSidebar from '../components/SupplierSidebar';
import SupplierHeader from '../components/SupplierHeader';
import SupplierFooter from '../components/SupplierFooter';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function SupplierLayout() {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (user?.user_role?.name !== 'supplier') {
      navigate('/');
      return;
    }
  }, [isAuthenticated, user, navigate]);

  return (
    <>
      <SupplierHeader />
      <SupplierSidebar />
      <div className="body-content outer-top-vs mt-5" id="top-banner-and-menu">
        <Outlet />
      </div>
      <SupplierFooter />
    </>
  );
}
