import { useEffect } from 'react';

const LEGACY_SCRIPTS = [
  '/assets/js/jquery-1.11.1.min.js',
  '/assets/js/bootstrap.min.js',
  '/assets/js/bootstrap-hover-dropdown.min.js',
  '/assets/js/owl.carousel.min.js',
  '/assets/js/echo.min.js',
  '/assets/js/jquery.easing-1.3.min.js',
  '/assets/js/bootstrap-slider.min.js',
  '/assets/js/jquery.rateit.min.js',
  '/assets/js/lightbox.min.js',
  '/assets/js/bootstrap-select.min.js',
  '/assets/js/wow.min.js',
  '/assets/js/scripts.js',
  '/assets/js/application.js',
];

function appendScript(src) {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(`script[data-legacy-src="${src}"]`);

    if (existing) {
      resolve();
      return;
    }

    const script = document.createElement('script');
    script.src = src;
    script.async = false;
    script.dataset.legacySrc = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`Unable to load ${src}`));
    document.body.appendChild(script);
  });
}

export default function LegacyScriptLoader({ enabled }) {
  useEffect(() => {
    let cancelled = false;

    async function loadScripts() {
      if (!enabled || window.__MARAZZO_LEGACY_LOADED__) {
        return;
      }

      for (const src of LEGACY_SCRIPTS) {
        if (cancelled) {
          return;
        }

        await appendScript(src);
      }

      window.__MARAZZO_LEGACY_LOADED__ = true;
    }

    loadScripts().catch((error) => {
      console.error(error);
    });

    return () => {
      cancelled = true;
    };
  }, [enabled]);

  return null;
}
