/**
 * Styled confirmation modal to replace native confirm() dialogs
 * @param {boolean} show - Whether to show the modal
 * @param {string} title - Modal title
 * @param {string} message - Confirmation message
 * @param {string} confirmText - Text for confirm button (default "Confirm")
 * @param {string} cancelText - Text for cancel button (default "Cancel")
 * @param {string} confirmStyle - Bootstrap button style (default "danger")
 * @param {function} onConfirm - Called when user confirms
 * @param {function} onCancel - Called when user cancels
 */
export default function ConfirmModal({
  show,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmStyle = 'danger',
  onConfirm,
  onCancel,
}) {
  if (!show) return null;

  return (
    <>
      <div
        className="modal fade in"
        style={{ display: 'block' }}
        tabIndex="-1"
        role="dialog"
        onClick={(e) => {
          // Close on backdrop click
          if (e.target === e.currentTarget) onCancel();
        }}
      >
        <div className="modal-dialog modal-sm" role="document" style={{ marginTop: '15%' }}>
          <div className="modal-content" style={{ borderRadius: '6px', overflow: 'hidden' }}>
            <div className="modal-header" style={{ borderBottom: '1px solid #eee', padding: '15px 20px' }}>
              <button
                type="button"
                className="close"
                onClick={onCancel}
                aria-label="Close"
              >
                <span aria-hidden="true">&times;</span>
              </button>
              <h4 className="modal-title" style={{ fontSize: '18px', fontWeight: '600' }}>
                {title}
              </h4>
            </div>
            <div className="modal-body" style={{ padding: '20px' }}>
              <p style={{ margin: 0, fontSize: '14px', color: '#555' }}>{message}</p>
            </div>
            <div className="modal-footer" style={{ padding: '12px 20px', borderTop: '1px solid #eee' }}>
              <button
                type="button"
                className="btn btn-default"
                onClick={onCancel}
              >
                {cancelText}
              </button>
              <button
                type="button"
                className={`btn btn-${confirmStyle}`}
                onClick={onConfirm}
              >
                {confirmText}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="modal-backdrop fade in"></div>
    </>
  );
}
