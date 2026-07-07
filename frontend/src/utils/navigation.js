/**
 * Mirrors Django template active_header classes on top-bar account links.
 */
export function isTopNavActive(pathname, segment) {
  return pathname.includes(segment);
}

export function topNavLinkClass(pathname, segment) {
  return isTopNavActive(pathname, segment) ? 'active_header' : '';
}

/**
 * Navbar item active state for React Router paths.
 */
export function isNavItemActive(pathname, path) {
  const normalizedPathname = normalizePath(pathname);
  const normalizedPath = normalizePath(path);

  if (path === '/') {
    return normalizedPathname === '/';
  }

  return normalizedPathname === normalizedPath || normalizedPathname.startsWith(`${normalizedPath}/`);
}

export function navItemClass(pathname, path, extra = '') {
  const active = isNavItemActive(pathname, path);
  return [extra, active ? 'active' : ''].filter(Boolean).join(' ');
}

export function categoryNavPath(categoryName) {
  return `/category/${encodeURIComponent(categoryName)}`;
}

export function isAnyNavPathActive(pathname, paths = []) {
  return paths.some((path) => isNavItemActive(pathname, path));
}

function normalizePath(path) {
  if (!path || path === '/') {
    return '/';
  }

  return path.replace(/\/+$/, '');
}
