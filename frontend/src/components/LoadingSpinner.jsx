/**
 * Reusable loading spinner component
 * @param {string} message - Optional loading message
 * @param {boolean} fullPage - If true, centers in viewport
 * @param {string} size - 'sm', 'md', 'lg'
 */
export default function LoadingSpinner({ message = 'Loading...', fullPage = false, size = 'md' }) {
  const sizes = {
    sm: { spinner: '24px', border: '3px', fontSize: '13px' },
    md: { spinner: '40px', border: '4px', fontSize: '15px' },
    lg: { spinner: '56px', border: '5px', fontSize: '17px' },
  };

  const s = sizes[size] || sizes.md;

  const spinnerStyle = {
    width: s.spinner,
    height: s.spinner,
    border: `${s.border} solid #f3f3f3`,
    borderTop: `${s.border} solid #0f6cb2`,
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    margin: '0 auto 15px',
  };

  const containerStyle = fullPage
    ? {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        padding: '50px',
      }
    : {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 20px',
      };

  return (
    <>
      <style>
        {`@keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }`}
      </style>
      <div style={containerStyle}>
        <div style={spinnerStyle}></div>
        {message && (
          <p className="text-muted" style={{ fontSize: s.fontSize, margin: 0 }}>
            {message}
          </p>
        )}
      </div>
    </>
  );
}
