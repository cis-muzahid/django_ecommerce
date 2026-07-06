export const assetUrl = (path) => `/assets/${path.replace(/^\/+/, '')}`;

export function money(value, currency = '$') {
  if (value === null || value === undefined || value === '') {
    return `${currency}0`;
  }

  return `${currency}${value}`;
}

export function categoryName(category) {
  if (!category) {
    return '';
  }

  return typeof category === 'string' ? category : category.name;
}

export function categoryHref(category) {
  const name = categoryName(category);
  return name ? `/category/${encodeURIComponent(name)}` : '#';
}

export function categoryTreeNames(category) {
  if (!category) {
    return [];
  }

  const children = category.subcategories || category.children || [];
  return [
    categoryName(category),
    ...children.flatMap((child) => categoryTreeNames(child)),
  ].filter(Boolean);
}

export function productHref(product) {
  if (!product || !product.category) {
    return '#';
  }

  const name = categoryName(product.category);
  return name && product.slug ? `/category/${encodeURIComponent(name)}/${encodeURIComponent(product.slug)}` : '#';
}

export function productImage(product) {
  return product?.main_image || assetUrl('images/blank.gif');
}

export function bannerImage(banner) {
  return banner?.image_url || banner?.image || assetUrl('images/blank.gif');
}

export function ratingStars(rating) {
  const count = Math.round(Number(rating) || 0);
  return Array.from({ length: 5 }, (_, index) => index < count);
}

export function chunk(items, size) {
  const chunks = [];
  for (let index = 0; index < items.length; index += size) {
    chunks.push(items.slice(index, index + size));
  }
  return chunks;
}

export function stripHtml(value = '') {
  return value.replace(/<[^>]*>/g, '');
}
