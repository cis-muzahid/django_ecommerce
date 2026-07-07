import HeaderTop from './HeaderTop';
import HeaderMain from './HeaderMain';
import Navbar from './Navbar';
import { useLayout } from '../context/LayoutContext';

export default function Header() {
  const { categories } = useLayout();

  return (
    <header className="header-style-1 react-header">
      <HeaderTop />
      <HeaderMain categories={categories} />
      <Navbar categories={categories} />
    </header>
  );
}
