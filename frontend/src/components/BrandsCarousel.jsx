export default function BrandsCarousel() {
  const brands = [
    { id: 1, image: '/assets/images/brands/brand1.png', alt: 'Brand 1' },
    { id: 2, image: '/assets/images/brands/brand2.png', alt: 'Brand 2' },
    { id: 3, image: '/assets/images/brands/brand3.png', alt: 'Brand 3' },
    { id: 4, image: '/assets/images/brands/brand4.png', alt: 'Brand 4' },
    { id: 5, image: '/assets/images/brands/brand5.png', alt: 'Brand 5' },
    { id: 6, image: '/assets/images/brands/brand6.png', alt: 'Brand 6' },
    { id: 7, image: '/assets/images/brands/brand2.png', alt: 'Brand 2' },
    { id: 8, image: '/assets/images/brands/brand4.png', alt: 'Brand 4' },
    { id: 9, image: '/assets/images/brands/brand1.png', alt: 'Brand 1' },
    { id: 10, image: '/assets/images/brands/brand5.png', alt: 'Brand 5' },
  ];

  return (
    <div id="brands-carousel" className="logo-slider wow fadeInUp">
      <div className="logo-slider-inner">
        <div id="brand-slider" className="owl-carousel brand-slider custom-carousel owl-theme">
          {brands.map((brand, index) => (
            <div key={brand.id} className={`item ${index === 0 ? 'm-t-15' : index === 1 ? 'm-t-10' : ''}`}>
              <a href="#" className="image">
                <img 
                  data-echo={brand.image}
                  src="/assets/images/blank.gif"
                  alt={brand.alt}
                />
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
