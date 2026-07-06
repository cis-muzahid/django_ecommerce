import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { getCategories } from '../services/categoriesService';
import { getHomepageData } from '../services/homeApi';

const LayoutContext = createContext({
  categories: [],
  facilities: [],
  categoriesLoading: true,
});

export function useLayout() {
  return useContext(LayoutContext);
}

export function LayoutProvider({ children }) {
  const [categories, setCategories] = useState([]);
  const [facilities, setFacilities] = useState([]);
  const [categoriesLoading, setCategoriesLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadLayoutData() {
      try {
        const [categoriesData, homepageData] = await Promise.all([
          getCategories(),
          getHomepageData().catch(() => ({ facilities: [] })),
        ]);

        if (cancelled) {
          return;
        }

        setCategories(categoriesData || []);
        setFacilities(homepageData?.facilities || []);
      } catch (error) {
        console.error('Failed to load layout data:', error);
      } finally {
        if (!cancelled) {
          setCategoriesLoading(false);
        }
      }
    }

    loadLayoutData();

    return () => {
      cancelled = true;
    };
  }, []);

  const value = useMemo(
    () => ({ categories, facilities, categoriesLoading }),
    [categories, facilities, categoriesLoading],
  );

  return <LayoutContext.Provider value={value}>{children}</LayoutContext.Provider>;
}
