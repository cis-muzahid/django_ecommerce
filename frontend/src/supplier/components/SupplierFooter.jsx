export default function SupplierFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer id="footer" className="footer color-bg">
      <div className="footer-bottom">
        <div className="container">
          <div className="row">
            <div className="col-xs-12 col-sm-12 col-md-12 col-lg-12">
              <div className="copyright-text text-center">
                <p>Copyright © {currentYear}-{currentYear + 1} . All rights reserved.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
