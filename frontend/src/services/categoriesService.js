import apiClient from './apiClient';

// Cache for categories
let categoriesCache = null;
let categoriesPromise = null;

/**
 * Fetch categories with caching
 * This ensures categories are fetched only once and reused across all pages
 */
export async function getCategories() {
  // Return cached data if available
  if (categoriesCache) {
    return categoriesCache;
  }

  // Return existing promise if fetch is in progress
  if (categoriesPromise) {
    return categoriesPromise;
  }

  // Start new fetch
  categoriesPromise = fetchCategoriesFromAPI();

  try {
    categoriesCache = await categoriesPromise;
    return categoriesCache;
  } finally {
    categoriesPromise = null;
  }
}

async function fetchCategoriesFromAPI() {
  try {
    // Try to fetch category tree first (with nested structure)
    const response = await apiClient.get('/categories/tree/');
    return normalizeCategoryTree(response.data || []);
  } catch (treeError) {
    // Fallback to regular categories endpoint and build hierarchy manually
    const response = await apiClient.get('/categories/');
    const allCategories = response.data.results || response.data || [];
    
    // Build hierarchy manually - return only parent categories with nested subcategories
    const parentId = (category) => {
      if (!category?.parent_category) return null;
      return typeof category.parent_category === 'object'
        ? category.parent_category.id
        : category.parent_category;
    };

    const byParent = allCategories.reduce((groups, category) => {
      const key = parentId(category) || 'root';
      if (!groups[key]) groups[key] = [];
      groups[key].push(category);
      return groups;
    }, {});

    const buildTree = (parentKey) => {
      const cats = byParent[parentKey] || [];
      return cats.map((category) => ({
        ...category,
        subcategories: buildTree(category.id),
      }));
    };

    // Return only root/parent categories with their nested subcategories
    return normalizeCategoryTree(buildTree('root'));
  }
}

function normalizeCategoryTree(categories = []) {
  return categories.map((category) => {
    const nested = category.subcategories || category.children || [];

    return {
      ...category,
      subcategories: normalizeCategoryTree(nested),
    };
  });
}

/**
 * Clear the categories cache (useful for refresh)
 */
export function clearCategoriesCache() {
  categoriesCache = null;
  categoriesPromise = null;
}
