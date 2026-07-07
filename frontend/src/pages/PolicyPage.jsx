import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';

const pageContent = {
  faq: {
    title: 'Frequently Asked Questions',
    sections: [
      ['How do I place an order?', 'Add products to your cart, proceed to checkout, choose a delivery address, and complete payment.'],
      ['Can I track my order?', 'Yes. Open My Orders and use Track Order for the latest status.'],
      ['How do returns work?', 'Eligible delivered items can be returned or replaced from your order history.'],
    ],
  },
  terms: {
    title: 'Terms & Conditions',
    sections: [
      ['Orders', 'Orders are subject to product availability and successful payment authorization.'],
      ['Accounts', 'You are responsible for keeping your account details accurate and secure.'],
      ['Use of site', 'Customer-facing shopping features are provided for lawful personal use only.'],
    ],
  },
  privacy: {
    title: 'Privacy Policy',
    sections: [
      ['Data we use', 'We use account, address, cart, wishlist, and order details to operate the store.'],
      ['Security', 'Authentication uses protected API requests and token-based sessions.'],
      ['Choices', 'You can update your profile and address information from your account page.'],
    ],
  },
  returns: {
    title: 'Refund & Return Policy',
    sections: [
      ['Returns', 'Delivered items may be eligible for return or replacement from the order page.'],
      ['Refunds', 'Refunds are processed after a return request is reviewed and approved.'],
      ['Cancelled orders', 'Orders that have not shipped can be cancelled where allowed by their current status.'],
    ],
  },
  shipping: {
    title: 'Shipping Policy',
    sections: [
      ['Delivery', 'Shipping times vary by address and order status. Track your order for updates.'],
      ['Address accuracy', 'Please verify your delivery address before placing an order.'],
      ['Fees', 'Any shipping charges are shown in checkout before payment.'],
    ],
  },
};

export default function PolicyPage({ type = 'faq' }) {
  const content = pageContent[type] || pageContent.faq;

  return (
    <>
      <Breadcrumbs items={[{ label: content.title }]} />
      <div className="row">
        <div className="col-md-10 col-md-offset-1">
          <h2 className="section-title">{content.title}</h2>
          <div className="panel panel-default">
            <div className="panel-body" style={{ padding: '30px' }}>
              {content.sections.map(([heading, body]) => (
                <div key={heading} style={{ marginBottom: '24px' }}>
                  <h4 style={{ fontWeight: 600 }}>{heading}</h4>
                  <p className="text-muted" style={{ lineHeight: 1.8 }}>{body}</p>
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
