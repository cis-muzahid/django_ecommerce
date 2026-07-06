import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

/**
 * Re-initialize bootstrap-hover-dropdown after React renders navigation markup.
 * Matches Django footer.html behavior for data-hover="dropdown" elements.
 */
export default function useHoverDropdown(dependencies = []) {
  const location = useLocation();

  useEffect(() => {
    if (!window.$ || !window.$.fn.dropdownHover) {
      return undefined;
    }

    const selector = '[data-hover="dropdown"]';
    window.$(selector).off('mouseenter mouseleave');
    window.$(selector).dropdownHover({
      delay: 500,
      instantlyCloseOthers: true,
    });

    return () => {
      window.$(selector).off('mouseenter mouseleave');
    };
  }, [location.pathname, ...dependencies]);
}
