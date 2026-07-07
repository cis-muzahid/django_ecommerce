import { useState } from 'react';
import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';

export default function ContactPage() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [notice, setNotice] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.subject || !form.message) {
      setNotice({ type: 'danger', text: 'Please fill in all fields' });
      return;
    }

    setSubmitting(true);
    // Simulate submission (no backend endpoint for contact form)
    setTimeout(() => {
      setNotice({ type: 'success', text: 'Thank you for contacting us! We will get back to you shortly.' });
      setForm({ name: '', email: '', subject: '', message: '' });
      setSubmitting(false);
    }, 1000);
  };

  return (
    <>
      <Breadcrumbs items={[{ label: 'Contact Us' }]} />

      <div className="row" style={{ marginBottom: '30px' }}>
        {/* Contact Form */}
        <div className="col-md-8">
          <div
            className="panel panel-default"
            style={{ border: 'none', boxShadow: '0 2px 10px rgba(0,0,0,0.06)' }}
          >
            <div className="panel-heading" style={{ background: '#fff', borderBottom: '2px solid #0f6cb2' }}>
              <h3 className="panel-title" style={{ fontWeight: '600', fontSize: '18px' }}>
                <i className="fa fa-envelope-o" style={{ marginRight: '8px' }}></i>
                Send Us a Message
              </h3>
            </div>
            <div className="panel-body" style={{ padding: '30px' }}>
              {notice && (
                <div className={`alert alert-${notice.type}`} role="alert">
                  {notice.text}
                </div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title" htmlFor="contact-name">
                        Your Name <span className="text-danger">*</span>
                      </label>
                      <input
                        type="text"
                        className="form-control unicase-form-control text-input"
                        id="contact-name"
                        name="name"
                        placeholder="Enter your name"
                        value={form.name}
                        onChange={handleChange}
                        required
                        disabled={submitting}
                      />
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title" htmlFor="contact-email">
                        Your Email <span className="text-danger">*</span>
                      </label>
                      <input
                        type="email"
                        className="form-control unicase-form-control text-input"
                        id="contact-email"
                        name="email"
                        placeholder="Enter your email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        disabled={submitting}
                      />
                    </div>
                  </div>
                </div>

                <div className="form-group">
                  <label className="info-title" htmlFor="contact-subject">
                    Subject <span className="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="contact-subject"
                    name="subject"
                    placeholder="What is this about?"
                    value={form.subject}
                    onChange={handleChange}
                    required
                    disabled={submitting}
                  />
                </div>

                <div className="form-group">
                  <label className="info-title" htmlFor="contact-message">
                    Message <span className="text-danger">*</span>
                  </label>
                  <textarea
                    className="form-control unicase-form-control"
                    id="contact-message"
                    name="message"
                    rows="6"
                    placeholder="Write your message here..."
                    value={form.message}
                    onChange={handleChange}
                    required
                    disabled={submitting}
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary btn-lg"
                  disabled={submitting}
                  style={{ padding: '10px 40px' }}
                >
                  {submitting ? (
                    <>
                      <i className="fa fa-spinner fa-spin"></i> Sending...
                    </>
                  ) : (
                    <>
                      <i className="fa fa-paper-plane"></i> Send Message
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Contact Info Sidebar */}
        <div className="col-md-4">
          <div
            className="panel panel-default"
            style={{ border: 'none', boxShadow: '0 2px 10px rgba(0,0,0,0.06)' }}
          >
            <div className="panel-heading" style={{ background: '#fff', borderBottom: '2px solid #0f6cb2' }}>
              <h3 className="panel-title" style={{ fontWeight: '600', fontSize: '18px' }}>
                <i className="fa fa-map-marker" style={{ marginRight: '8px' }}></i>
                Get in Touch
              </h3>
            </div>
            <div className="panel-body" style={{ padding: '25px' }}>
              {[
                {
                  icon: 'fa-map-marker',
                  title: 'Address',
                  content: 'ThemesGround, 789 Main rd, Anytown, CA 12345 USA',
                },
                {
                  icon: 'fa-phone',
                  title: 'Phone',
                  content: '+ (888) 123-4567\n+ (888) 456-7890',
                },
                {
                  icon: 'fa-envelope',
                  title: 'Email',
                  content: 'marazzo@themesground.com',
                },
                {
                  icon: 'fa-clock-o',
                  title: 'Business Hours',
                  content: 'Mon - Fri: 9:00 AM - 6:00 PM\nSat: 10:00 AM - 4:00 PM\nSun: Closed',
                },
              ].map((item) => (
                <div
                  key={item.title}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    marginBottom: '20px',
                    paddingBottom: '20px',
                    borderBottom: '1px solid #f0f0f0',
                  }}
                >
                  <div
                    style={{
                      width: '40px',
                      height: '40px',
                      borderRadius: '50%',
                      background: '#0f6cb2',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                      marginRight: '12px',
                    }}
                  >
                    <i className={`fa ${item.icon}`} style={{ color: '#fff', fontSize: '16px' }}></i>
                  </div>
                  <div>
                    <h5 style={{ fontWeight: '600', marginBottom: '5px', fontSize: '14px' }}>
                      {item.title}
                    </h5>
                    <p
                      className="text-muted"
                      style={{ margin: 0, fontSize: '13px', whiteSpace: 'pre-line' }}
                    >
                      {item.content}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Social Links */}
          <div
            className="panel panel-default"
            style={{
              border: 'none',
              boxShadow: '0 2px 10px rgba(0,0,0,0.06)',
              marginTop: '20px',
            }}
          >
            <div className="panel-body text-center" style={{ padding: '25px' }}>
              <h5 style={{ fontWeight: '600', marginBottom: '15px' }}>Follow Us</h5>
              <div>
                {[
                  { icon: 'fa-facebook', color: '#3b5998', url: 'https://facebook.com' },
                  { icon: 'fa-twitter', color: '#1da1f2', url: 'https://twitter.com' },
                  { icon: 'fa-instagram', color: '#e4405f', url: 'https://instagram.com' },
                  { icon: 'fa-linkedin', color: '#0077b5', url: 'https://linkedin.com' },
                ].map((social) => (
                  <a
                    key={social.icon}
                    href={social.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: '40px',
                      height: '40px',
                      borderRadius: '50%',
                      background: social.color,
                      color: '#fff',
                      margin: '0 5px',
                      fontSize: '16px',
                      transition: 'opacity 0.2s',
                    }}
                  >
                    <i className={`fa ${social.icon}`}></i>
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <BrandsCarousel />
    </>
  );
}
