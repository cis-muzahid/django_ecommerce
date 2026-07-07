import { useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import InfoBox from './InfoBox';
import { LayoutProvider, useLayout } from '../context/LayoutContext';
import useHoverDropdown from '../hooks/useHoverDropdown';

function MainLayoutContent() {
  const { facilities } = useLayout();
  const location = useLocation();

  useHoverDropdown();

  useEffect(() => {
    document.body.classList.add('cnt-home');
    return () => {
      document.body.classList.remove('cnt-home');
    };
  }, []);

  return (
    <>
      <Header />
      <div className="body-content outer-top-vs" id="top-banner-and-menu" key={location.pathname}>
        <div className="container">
          <Outlet />
        </div>
      </div>
      <InfoBox facilities={facilities} />
      <Footer />
    </>
  );
}

export default function MainLayout() {
  return (
    <LayoutProvider>
      <MainLayoutContent />
    </LayoutProvider>
  );
}
