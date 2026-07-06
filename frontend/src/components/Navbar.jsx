import { useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import useHoverDropdown from '../hooks/useHoverDropdown';
import {
  categoryNavPath,
  isAnyNavPathActive,
  isNavItemActive,
  navItemClass,
} from '../utils/navigation';

export default function Navbar({ categories = [] }) {
  const navigate = useNavigate();
  const location = useLocation();
  const pathname = location.pathname;
  const [navCollapsed, setNavCollapsed] = useState(true);
  const [openCategoryId, setOpenCategoryId] = useState(null);

  useHoverDropdown([categories]);

  function navigateTo(event, path) {
    event.preventDefault();
    navigate(path);
    setNavCollapsed(true);
    setOpenCategoryId(null);
  }

  function toggleDropdown(event, categoryId) {
    event.preventDefault();
    setOpenCategoryId((currentId) => (currentId === categoryId ? null : categoryId));
  }

  function getSubcategories(category) {
    return category.subcategories || category.children || [];
  }

  function isCategoryActive(categoryName) {
    return isNavItemActive(pathname, categoryNavPath(categoryName));
  }

  function hasActiveDescendant(category) {
    return getSubcategories(category).some(
      (subcategory) => isCategoryActive(subcategory.name) || hasActiveDescendant(subcategory),
    );
  }

  return (
    <div className="header-nav animate-dropdown">
      <div className="container">
        <div className="yamm navbar navbar-default" role="navigation">
          <div className="navbar-header">
            <button
              data-target="#mc-horizontal-menu-collapse"
              data-toggle="collapse"
              className={`navbar-toggle ${navCollapsed ? 'collapsed' : ''}`}
              type="button"
              onClick={() => setNavCollapsed((collapsed) => !collapsed)}
            >
              <span className="sr-only">Toggle navigation</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
          </div>
          <div className="nav-bg-class">
            <div
              className={`navbar-collapse collapse ${navCollapsed ? '' : 'in'}`}
              id="mc-horizontal-menu-collapse"
            >
              <div className="nav-outer">
                <ul className="nav navbar-nav">
                  <li className={navItemClass(pathname, '/', 'dropdown yamm mega-menu')}>
                    <a
                      href="/"
                      onClick={(event) => navigateTo(event, '/')}
                      data-hover="dropdown"
                    >
                      Home
                    </a>
                  </li>
                  {categories.map((category) => {
                    const subcategories = getSubcategories(category);
                    const hasSubcategories = subcategories.length > 0;
                    const categoryPath = categoryNavPath(category.name);
                    const active = isCategoryActive(category.name) || hasActiveDescendant(category);
                    const open = openCategoryId === category.id;

                    if (hasSubcategories) {
                      return (
                        <li
                          className={`dropdown yamm mega-menu${active ? ' active' : ''}${open ? ' open' : ''}`}
                          key={category.id}
                          onMouseEnter={() => setOpenCategoryId(category.id)}
                          onMouseLeave={() => setOpenCategoryId(null)}
                        >
                          <a
                            href={categoryPath}
                            onClick={(event) => toggleDropdown(event, category.id)}
                            className="dropdown-toggle"
                            data-hover="dropdown"
                            data-toggle="dropdown"
                          >
                            {category.name}
                          </a>
                          <ul className="dropdown-menu container">
                            <li>
                              <div className="yamm-content">
                                <div className="row">
                                  {subcategories.map((subcategory) => {
                                    const nestedSubcategories = getSubcategories(subcategory);
                                    const hasSubSubcategories = nestedSubcategories.length > 0;

                                    if (hasSubSubcategories) {
                                      return (
                                        <div
                                          className="col-xs-12 col-sm-6 col-md-2 col-menu"
                                          key={subcategory.id}
                                        >
                                          <h2 className="title">
                                            <a
                                              href={categoryNavPath(subcategory.name)}
                                              onClick={(event) =>
                                                navigateTo(
                                                  event,
                                                  categoryNavPath(subcategory.name),
                                                )
                                              }
                                            >
                                              {subcategory.name}
                                            </a>
                                          </h2>
                                          <ul className="links">
                                            {nestedSubcategories.map((sub) => (
                                              <li key={sub.id}>
                                                <a
                                                  href={categoryNavPath(sub.name)}
                                                  onClick={(event) =>
                                                    navigateTo(
                                                      event,
                                                      categoryNavPath(sub.name),
                                                    )
                                                  }
                                                >
                                                  {sub.name}
                                                </a>
                                              </li>
                                            ))}
                                          </ul>
                                        </div>
                                      );
                                    }

                                    return (
                                      <a
                                        key={subcategory.id}
                                        href={categoryNavPath(subcategory.name)}
                                        onClick={(event) =>
                                          navigateTo(
                                            event,
                                            categoryNavPath(subcategory.name),
                                          )
                                        }
                                      >
                                        {subcategory.name}
                                      </a>
                                    );
                                  })}
                                </div>
                              </div>
                            </li>
                          </ul>
                        </li>
                      );
                    }

                    return (
                      <li
                        className={`dropdown yamm mega-menu${active ? ' active' : ''}`}
                        key={category.id}
                      >
                        <a
                          href={categoryPath}
                          onClick={(event) => navigateTo(event, categoryPath)}
                          data-hover="dropdown"
                        >
                          {category.name}
                        </a>
                      </li>
                    );
                  })}
                  <li
                    className={[
                      'dropdown yamm mega-menu',
                      isAnyNavPathActive(pathname, ['/blogs', '/user/blogs', '/blog', '/user/blog'])
                        ? 'active'
                        : '',
                    ].filter(Boolean).join(' ')}
                  >
                    <a
                      href="/user/blogs"
                      onClick={(event) => navigateTo(event, '/user/blogs')}
                      data-hover="dropdown"
                    >
                      Blog
                    </a>
                  </li>
                  <li className="dropdown navbar-right special-menu">
                    <a href="#">Get 30% off on selected items</a>
                  </li>
                </ul>
                <div className="clearfix"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
