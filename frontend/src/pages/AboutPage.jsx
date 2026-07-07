import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';

export default function AboutPage() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'About Us' }]} />

      <div className="row">
        <div className="col-md-12">
          {/* Hero Section */}
          <div
            className="panel panel-default"
            style={{ border: 'none', boxShadow: '0 2px 10px rgba(0,0,0,0.06)' }}
          >
            <div className="panel-body text-center" style={{ padding: '50px 30px' }}>
              <h1 style={{ fontSize: '32px', fontWeight: '700', marginBottom: '15px', color: '#333' }}>
                About Marazzo eCommerce
              </h1>
              <p className="text-muted" style={{ fontSize: '16px', maxWidth: '700px', margin: '0 auto 30px' }}>
                We are a passionate team dedicated to bringing you the best online shopping experience.
                Since our founding, we have been committed to quality products, competitive prices,
                and outstanding customer service.
              </p>
            </div>
          </div>

          {/* Mission & Vision */}
          <div className="row" style={{ marginTop: '30px' }}>
            <div className="col-md-6">
              <div
                className="panel panel-default"
                style={{ border: 'none', boxShadow: '0 2px 10px rgba(0,0,0,0.06)' }}
              >
                <div className="panel-body" style={{ padding: '30px' }}>
                  <div className="text-center" style={{ marginBottom: '20px' }}>
                    <i className="fa fa-bullseye" style={{ fontSize: '40px', color: '#0f6cb2' }}></i>
                  </div>
                  <h3 className="text-center" style={{ fontWeight: '600', marginBottom: '15px' }}>
                    Our Mission
                  </h3>
                  <p className="text-muted" style={{ lineHeight: '1.8' }}>
                    To provide an exceptional online shopping experience by offering a curated
                    selection of high-quality products at competitive prices. We strive to make
                    e-commerce accessible, enjoyable, and secure for everyone.
                  </p>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div
                className="panel panel-default"
                style={{ border: 'none', boxShadow: '0 2px 10px rgba(0,0,0,0.06)' }}
              >
                <div className="panel-body" style={{ padding: '30px' }}>
                  <div className="text-center" style={{ marginBottom: '20px' }}>
                    <i className="fa fa-eye" style={{ fontSize: '40px', color: '#0f6cb2' }}></i>
                  </div>
                  <h3 className="text-center" style={{ fontWeight: '600', marginBottom: '15px' }}>
                    Our Vision
                  </h3>
                  <p className="text-muted" style={{ lineHeight: '1.8' }}>
                    To become the most trusted and preferred online marketplace, known for
                    innovation, reliability, and a deep commitment to customer satisfaction.
                    We envision a world where shopping is effortless and enjoyable.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Values */}
          <div style={{ marginTop: '30px' }}>
            <h2 className="text-center" style={{ fontWeight: '600', marginBottom: '30px' }}>
              Why Choose Us
            </h2>
            <div className="row">
              {[
                {
                  icon: 'fa-truck',
                  title: 'Fast Delivery',
                  desc: 'We ensure quick and reliable delivery of your orders right to your doorstep.',
                },
                {
                  icon: 'fa-shield',
                  title: 'Secure Shopping',
                  desc: 'Your data and transactions are protected with industry-standard encryption.',
                },
                {
                  icon: 'fa-refresh',
                  title: 'Easy Returns',
                  desc: 'Not satisfied? Our hassle-free return policy makes it easy to return or exchange.',
                },
                {
                  icon: 'fa-headphones',
                  title: '24/7 Support',
                  desc: 'Our dedicated customer support team is always here to help you with any queries.',
                },
              ].map((item) => (
                <div className="col-md-3 col-sm-6" key={item.title}>
                  <div
                    className="text-center"
                    style={{
                      padding: '30px 15px',
                      background: '#fff',
                      borderRadius: '6px',
                      boxShadow: '0 2px 10px rgba(0,0,0,0.06)',
                      marginBottom: '20px',
                    }}
                  >
                    <i
                      className={`fa ${item.icon}`}
                      style={{ fontSize: '36px', color: '#0f6cb2', marginBottom: '15px', display: 'block' }}
                    ></i>
                    <h4 style={{ fontWeight: '600', marginBottom: '10px' }}>{item.title}</h4>
                    <p className="text-muted" style={{ fontSize: '13px' }}>{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div
            style={{
              marginTop: '30px',
              padding: '40px 0',
              background: '#0f6cb2',
              borderRadius: '6px',
              marginBottom: '30px',
            }}
          >
            <div className="row text-center" style={{ color: '#fff' }}>
              {[
                { number: '10K+', label: 'Happy Customers' },
                { number: '5K+', label: 'Products' },
                { number: '100+', label: 'Brands' },
                { number: '50+', label: 'Categories' },
              ].map((stat) => (
                <div className="col-md-3 col-sm-6" key={stat.label}>
                  <h2 style={{ fontWeight: '700', fontSize: '36px', marginBottom: '5px' }}>
                    {stat.number}
                  </h2>
                  <p style={{ opacity: 0.85, fontSize: '14px' }}>{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <BrandsCarousel />
    </>
  );
}
