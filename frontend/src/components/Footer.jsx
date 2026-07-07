export default function Footer() {
  return (
    <footer id="footer" className="footer color-bg">
      <div className="footer-bottom">
        <div className="container">
          <div className="row">
            <div className="col-xs-12 col-sm-6 col-md-3">
              <div className="address-block">
                <div className="module-body">
                  <ul className="toggle-footer">
                    <li className="media">
                      <div className="pull-left">
                        <span className="icon fa-stack fa-lg">
                          <i className="fa fa-map-marker fa-stack-1x fa-inverse"></i>
                        </span>
                      </div>
                      <div className="media-body">
                        <p>ThemesGround, 789 Main rd, Anytown, CA 12345 USA</p>
                      </div>
                    </li>
                    <li className="media">
                      <div className="pull-left">
                        <span className="icon fa-stack fa-lg">
                          <i className="fa fa-mobile fa-stack-1x fa-inverse"></i>
                        </span>
                      </div>
                      <div className="media-body">
                        <p> + (888) 123-4567 / + (888) 456-7890</p>
                      </div>
                    </li>
                    <li className="media">
                      <div className="pull-left">
                        <span className="icon fa-stack fa-lg">
                          <i className="fa fa-envelope fa-stack-1x fa-inverse"></i>
                        </span>
                      </div>
                      <div className="media-body">
                        <span>
                          <a href="#">marazzo@themesground.com</a>
                        </span>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {[
              ['Customer Service', ['My Account', 'Order History', 'FAQ', 'Specials', 'Help Center']],
              ['Corporation', ['About us', 'Customer Service', 'Company', 'Investor Relations', 'Advanced Search']],
              ['Why Choose Us', ['Shopping Guide', 'Blog', 'Company', 'Investor Relations', 'Contact Us']],
            ].map(([title, links]) => (
              <div className="col-xs-12 col-sm-6 col-md-3" key={title}>
                <div className="module-heading">
                  <h4 className="module-title">{title}</h4>
                </div>
                <div className="module-body">
                  <ul className="list-unstyled">
                    {links.map((link, index) => (
                      <li
                        key={link}
                        className={
                          index === 0 ? 'first' : index === links.length - 1 ? 'last' : ''
                        }
                      >
                        <a href="#" title={link}>
                          {link}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="copyright-bar">
        <div className="container">
          <div className="col-xs-12 col-sm-4 no-padding social">
            <ul className="link">
              <li className="fb pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://www.facebook.com" title="Facebook"></a>
              </li>
              <li className="tw pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://twitter.com" title="Twitter"></a>
              </li>
              <li className="googleplus pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://plus.google.com" title="GooglePlus"></a>
              </li>
              <li className="rss pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://yourwebsite.com/rss" title="RSS"></a>
              </li>
              <li className="pintrest pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://www.pinterest.com" title="PInterest"></a>
              </li>
              <li className="linkedin pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://www.linkedin.com" title="Linkedin"></a>
              </li>
              <li className="youtube pull-left">
                <a target="_blank" rel="nofollow noreferrer" href="https://www.youtube.com" title="Youtube"></a>
              </li>
            </ul>
          </div>
          <div className="col-xs-12 col-sm-4 no-padding copyright">
            <a target="_blank" rel="noreferrer" href="https://www.templateshub.net">
              Happy Shopping
            </a>
          </div>
          <div className="col-xs-12 col-sm-4 no-padding">
            <div className="clearfix payment-methods">
              <ul>
                {[1, 2, 3, 4, 5].map((number) => (
                  <li key={number}>
                    <img src={`/assets/images/payments/${number}.png`} alt="" />
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
