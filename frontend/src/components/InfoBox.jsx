export default function InfoBox({ facilities = [] }) {
  return (
    <div className="row our-features-box">
      <div className="container text-center">
        {facilities && facilities.length > 0 ? (
          <ul className="facility_ul">
            {facilities.map((facility) => (
              <li key={facility.id}>
                <div className="feature-box">
                  <div>
                    <img 
                      src={facility.image_url || `/media/${facility.image}`} 
                      className="img-rounded image-responsive" 
                      style={{ width: '50px', height: '30px' }} 
                      alt={facility.title}
                    />
                  </div>
                  <div className="content-blocks">{facility.title}</div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No data Found</p>
        )}
      </div>
    </div>
  );
}
