import { Link, useLocation } from 'react-router-dom';
import { categoryNavPath, isNavItemActive } from '../utils/navigation';
import useHoverDropdown from '../hooks/useHoverDropdown';

/**
 * Reusable category sidebar column — matches Django side-menu on home/category pages.
 */
export default function Sidebar({ categories = [], children = null, className = '' }) {
  const location = useLocation();
  const parentCategories = categories.filter((category) => !category.parent_category);

  useHoverDropdown([categories]);

  function getSubcategories(category) {
    return category.subcategories || category.children || [];
  }

  function isCategoryActive(categoryName) {
    return isNavItemActive(location.pathname, categoryNavPath(categoryName));
  }

  function hasActiveDescendant(category) {
    return getSubcategories(category).some(
      (subcategory) => isCategoryActive(subcategory.name) || hasActiveDescendant(subcategory),
    );
  }

  return (
    <div className={`col-xs-12 col-sm-12 col-md-3 sidebar ${className}`.trim()}>
      <div className="side-menu animate-dropdown outer-bottom-xs">
        <div className="head">
          <i className="icon fa fa-align-justify fa-fw"></i> Categories
        </div>
        <nav className="yamm megamenu-horizontal">
          <ul className="nav">
            {parentCategories.map((category) => {
              const subcategories = getSubcategories(category);
              const hasSubcategories = subcategories.length > 0;
              const active = isCategoryActive(category.name) || hasActiveDescendant(category);

              if (hasSubcategories) {
                return (
                  <li className={`dropdown menu-item${active ? ' active' : ''}`} key={category.id}>
                    <a
                      href={categoryNavPath(category.name)}
                      className="dropdown-toggle"
                      data-toggle="dropdown"
                      data-hover="dropdown"
                      onClick={(event) => event.preventDefault()}
                    >
                      <i className="icon fa fa-shopping-bag" aria-hidden="true"></i>
                      {category.name}
                    </a>
                    <ul className="dropdown-menu mega-menu">
                      <div className="row">
                        {subcategories.map((subcategory) => (
                          <div className="col-sm-12 col-md-3" key={subcategory.id}>
                            <ul className="links list-unstyled">
                              <li>
                                <Link to={categoryNavPath(subcategory.name)}>
                                  <b>{subcategory.name}</b>
                                </Link>
                              </li>
                              {getSubcategories(subcategory).map((sub) => (
                                <li key={sub.id}>
                                  <Link to={categoryNavPath(sub.name)}>{sub.name}</Link>
                                </li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    </ul>
                  </li>
                );
              }

              return (
                <li className={`dropdown menu-item${active ? ' active' : ''}`} key={category.id}>
                  <Link to={categoryNavPath(category.name)}>
                    <i className="icon fa fa-shopping-bag" aria-hidden="true"></i>
                    {category.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
      {children}
    </div>
  );
}
