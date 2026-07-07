import { useEffect, useMemo, useState } from 'react';
import HomeSidebar from '../components/HomeSidebar.jsx';
import ProductCard from '../components/ProductCard.jsx';
import { getHomepageData } from '../services/homeApi.js';
import { useAuth } from '../context/AuthContext.jsx';
import { useCart } from '../context/CartContext.jsx';
import { useLayout } from '../context/LayoutContext.jsx';
import {
  bannerImage,
  categoryHref,
  categoryName,
  categoryTreeNames,
  productHref,
  stripHtml,
} from '../utils/catalog.js';

const EMPTY_HOME = {
  banners: {},
  latest_products: [],
  special_offers: {},
  hot_deals: [],
  categories: [],
  blogs: [],
  facilities: [],
};

function EmptyBox() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 230, backgroundColor: 'white' }}>
      <div className="inner-container">
        <p className="text-center">No Data Found</p>
      </div>
    </div>
  );
}

function Hero({ banners }) {
  return (
    <div id="hero">
      <div id="owl-main" className="owl-carousel owl-inner-nav owl-ui-sm">
        {banners.length ? banners.map((banner) => (
          <div className="item" style={{ backgroundImage: `url('${bannerImage(banner)}')` }} key={banner.id}>
            <div className="container-fluid">
              <div className="caption bg-color vertical-center text-left header_text_div">
                <div className="slider-header fadeInDown-1" style={{ color: 'white', fontWeight: 400 }}>{banner.subtitle}</div>
                <div className="big-text fadeInDown-1" style={{ color: 'white' }}>{banner.title}</div>
                <div className="excerpt fadeInDown-2 hidden-xs" style={{ color: 'white', fontWeight: 400 }}>
                  <span>"{banner.description}"</span>
                </div>
                <div className="button-holder fadeInDown-3">
                  <a href={categoryHref(banner.category)} className="btn-lg btn btn-uppercase btn-primary shop-now-button">Shop Now</a>
                </div>
              </div>
            </div>
          </div>
        )) : (
          <div className="item" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div className="inner-container"><h3 className="text-center">No Data Found</h3></div>
          </div>
        )}
      </div>
    </div>
  );
}

function ProductCarousel({ products, isAuthenticated, onAddCart, onAddWishlist, className = 'owl-carousel home-owl-carousel custom-carousel owl-theme' }) {
  if (!products.length) {
    return <EmptyBox />;
  }

  return (
    <div className={className}>
      {products.map((product) => (
        <ProductCard
          product={product}
          isAuthenticated={isAuthenticated}
          onAddCart={onAddCart}
          onAddWishlist={onAddWishlist}
          key={product.id}
        />
      ))}
    </div>
  );
}

function NewProductsTabs({ categories, products, isAuthenticated, onAddCart, onAddWishlist }) {
  return (
    <div id="product-tabs-slider" className="scroll-tabs outer-top-vs">
      <div className="more-info-tab clearfix ">
        <h3 className="new-product-title pull-left">New Products</h3>
        <ul className="nav nav-tabs nav-tab-line pull-right" id="new-products-1">
          <li className="active"><a data-transition-type="backSlide" href="#all" data-toggle="tab">All</a></li>
          {categories.map((category) => (
            <li key={category.id}><a data-transition-type="backSlide" href={`#category-${category.id}`} data-toggle="tab">{category.name}</a></li>
          ))}
        </ul>
      </div>
      <div className="tab-content outer-top-xs">
        <div className="tab-pane in active" id="all">
          <div className="product-slider">
            <ProductCarousel products={products} isAuthenticated={isAuthenticated} onAddCart={onAddCart} onAddWishlist={onAddWishlist} />
          </div>
        </div>
        {categories.map((category) => {
          const categoryNames = new Set(categoryTreeNames(category));
          const categoryProducts = products.filter((product) => categoryNames.has(categoryName(product.category)));
          return (
            <div className="tab-pane" id={`category-${category.id}`} key={category.id}>
              <div className="product-slider">
                <ProductCarousel products={categoryProducts} isAuthenticated={isAuthenticated} onAddCart={onAddCart} onAddWishlist={onAddWishlist} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function MiddleBanners({ banners }) {
  return (
    <div className="wide-banners outer-bottom-xs">
      <div className="row">
        {banners.map((banner) => (
          <div className="col-md-4" key={banner.id}>
            <div style={{ width: 440, height: 230, background: `url('${bannerImage(banner)}')`, backgroundSize: 'cover' }}>
              <div className="card-body">
                <div className="text-left mt-3" style={{ paddingLeft: '10%', paddingTop: '12%' }}>
                  <div className="slider-header fadeInDown-1" style={{ color: 'white', fontWeight: 400, fontSize: 'large' }}>{banner.subtitle}</div>
                  <div style={{ color: 'white', fontSize: 'xx-large', fontWeight: 600 }}>{banner.title}</div>
                  <div className="excerpt fadeInDown-2 hidden-xs" style={{ color: 'white', fontWeight: 400 }}>
                    <span>"{banner.description}"</span>
                  </div>
                  <br />
                  <div className="button-holder fadeInDown-3">
                    <a href={categoryHref(banner.category)} className="btn-lg btn btn-uppercase btn-primary shop-now-button">Shop Now</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function FeaturedStrip({ products, categories, isAuthenticated, onAddCart, onAddWishlist }) {
  const electronicsChildren = categories.find((category) => category.name.toLowerCase() === 'electronics')?.subcategories || [];
  const electronicsProducts = products.filter((product) => categoryName(product.category).toLowerCase().includes('electronics'));
  const displayProducts = electronicsProducts.length ? electronicsProducts : products.slice(0, 8);

  return (
    <section className="section featured-product">
      <div className="row">
        <div className="col-lg-3">
          <h3 className="section-title">Electronics & Digital</h3>
          <ul className="sub-cat">
            {electronicsChildren.map((category) => (
              <li key={category.id}><a href={categoryHref(category)}>{category.name}</a></li>
            ))}
          </ul>
        </div>
        <div className="col-lg-9">
          <ProductCarousel
            products={displayProducts}
            isAuthenticated={isAuthenticated}
            onAddCart={onAddCart}
            onAddWishlist={onAddWishlist}
            className="owl-carousel homepage-owl-carousel custom-carousel owl-theme outer-top-xs"
          />
        </div>
      </div>
    </section>
  );
}

function WideBanner({ large, small }) {
  return (
    <div className="wide-banners outer-bottom-xs">
      <div className="row">
        <div className="col-md-8">
          {large ? (
            <div className="wide-banner1 cnt-strip">
              <div className="image"><img className="img-responsive" src={bannerImage(large)} alt="" style={{ height: 230, width: '100%' }} /></div>
              <div className="strip strip-text">
                <div className="strip-inner">
                  <h2 className="text-right">
                    {large.title}
                    <br />
                    <span className="shopping-needs">{large.description}</span>
                    <br />
                    <div className="button-holder fadeInDown-3">
                      <a href={categoryHref(large.category)} className="btn-lg btn btn-uppercase btn-primary shop-now-button">Shop Now</a>
                    </div>
                  </h2>
                </div>
              </div>
              <div className="new-label"><div className="text">NEW</div></div>
            </div>
          ) : <EmptyBox />}
        </div>
        <div className="col-md-4">
          {small ? (
            <div className="wide-banner cnt-strip">
              <div className="image"><img className="img-responsive" src={bannerImage(small)} alt="" style={{ height: 230, width: '100%' }} /></div>
              <div className="strip strip-text">
                <div className="strip-inner">
                  <h2 className="text-right">
                    {small.title}
                    <br />
                    <span className="shopping-needs">{small.description}</span>
                    <br />
                    <div className="button-holder fadeInDown-3">
                      <a href={categoryHref(small.category)} className="btn-lg btn btn-uppercase btn-primary shop-now-button">Shop Now</a>
                    </div>
                  </h2>
                </div>
              </div>
            </div>
          ) : <EmptyBox />}
        </div>
      </div>
    </div>
  );
}

function BlogSlider({ blogs }) {
  return (
    <section className="section latest-blog outer-bottom-vs">
      <h3 className="section-title">Latest form Blog</h3>
      <div className="blog-slider-container outer-top-xs">
        {blogs.length ? (
          <div className="owl-carousel blog-slider custom-carousel">
            {blogs.map((blog) => (
              <div className="item" key={blog.id}>
                <div className="blog-post">
                  <div className="blog-post-image">
                    <div className="image">
                      <a href={`/user/blog/${blog.id}`}>
                        <img src={blog.image_url || blog.image} alt={`${blog.title} image`} style={{ height: 230 }} />
                      </a>
                    </div>
                  </div>
                  <div className="blog-post-info text-left">
                    <h3 className="name"><a href={`/user/blog/${blog.id}`}>{blog.title}</a></h3>
                    <span className="info">By {blog.user?.first_name} {blog.user?.last_name} &nbsp;|&nbsp; 21 March 2016 </span>
                    <p className="text">{stripHtml(blog.excerpt || '')}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : <EmptyBox />}
      </div>
    </section>
  );
}

function BrandsCarousel() {
  const brands = ['brand1.png', 'brand2.png', 'brand3.png', 'brand4.png', 'brand5.png', 'brand6.png', 'brand2.png', 'brand4.png', 'brand1.png', 'brand5.png'];

  return (
    <div id="brands-carousel" className="logo-slider">
      <div className="logo-slider-inner">
        <div id="brand-slider" className="owl-carousel brand-slider custom-carousel owl-theme">
          {brands.map((brand, index) => (
            <div className={`item ${index === 0 ? 'm-t-15' : index === 1 ? 'm-t-10' : ''}`} key={`${brand}-${index}`}>
              <a href="#" className="image">
                <img data-echo={`/assets/images/brands/${brand}`} src="/assets/images/blank.gif" alt="" />
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [homeData, setHomeData] = useState(EMPTY_HOME);
  const [isReady, setIsReady] = useState(false);
  const { categories } = useLayout();
  const { isAuthenticated } = useAuth();
  const { addToCart, addToWishlist } = useCart();

  const specialOffers = useMemo(() => {
    const groups = homeData.special_offers || {};
    return [
      ...(groups.products_1 || []),
      ...(groups.products_2 || []),
      ...(groups.products_3 || []),
    ];
  }, [homeData.special_offers]);

  useEffect(() => {
    async function loadData() {
      const homepageData = await getHomepageData();

      setHomeData(homepageData);

      setIsReady(true);
    }

    loadData().catch((error) => {
      console.error(error);
      setIsReady(true);
    });
  }, [isAuthenticated]);

  // Initialize Owl Carousels after data is loaded and DOM is ready
  useEffect(() => {
    if (!isReady || !homeData.banners) return;

    const initCarousels = () => {
      if (typeof window.$ === 'undefined' || typeof window.$.fn.owlCarousel === 'undefined') {
        console.warn('jQuery or Owl Carousel not loaded');
        return;
      }

      // Hero/Main banner carousel
      const $owlMain = window.$('#owl-main');
      if ($owlMain.length && !$owlMain.hasClass('owl-loaded')) {
        $owlMain.owlCarousel({
          navigation: true,
          slideSpeed: 300,
          paginationSpeed: 400,
          singleItem: true,
          navigationText: ['<a class="left carousel-control">‹</a>', '<a class="right carousel-control">›</a>'],
          autoPlay: true
        });
      }

      // Home product carousels
      window.$('.home-owl-carousel').each(function() {
        const $this = window.$(this);
        if (!$this.hasClass('owl-loaded')) {
          $this.owlCarousel({
            navigation: true,
            navigationText: ['<a class="left carousel-control">‹</a>', '<a class="right carousel-control">›</a>'],
            slideSpeed: 300,
            paginationSpeed: 400,
            items: 4,
            itemsDesktop: [1199, 3],
            itemsDesktopSmall: [979, 3],
            itemsTablet: [768, 2],
            itemsMobile: [479, 1],
            autoPlay: false
          });
        }
      });

      // Sidebar carousels
      window.$('.sidebar-carousel').each(function() {
        const $this = window.$(this);
        if (!$this.hasClass('owl-loaded')) {
          $this.owlCarousel({
            navigation: true,
            navigationText: ['<a class="left carousel-control">‹</a>', '<a class="right carousel-control">›</a>'],
            slideSpeed: 300,
            paginationSpeed: 400,
            singleItem: true,
            autoPlay: true
          });
        }
      });

      // Brand slider
      const $brandSlider = window.$('#brand-slider');
      if ($brandSlider.length && !$brandSlider.hasClass('owl-loaded')) {
        $brandSlider.owlCarousel({
          navigation: true,
          navigationText: ['<a class="left carousel-control">‹</a>', '<a class="right carousel-control">›</a>'],
          slideSpeed: 300,
          paginationSpeed: 400,
          items: 6,
          itemsDesktop: [1199, 5],
          itemsDesktopSmall: [979, 4],
          itemsTablet: [768, 3],
          itemsMobile: [479, 2],
          autoPlay: true
        });
      }

      // Blog slider
      window.$('.blog-slider').each(function() {
        const $this = window.$(this);
        if (!$this.hasClass('owl-loaded')) {
          $this.owlCarousel({
            navigation: true,
            navigationText: ['<a class="left carousel-control">‹</a>', '<a class="right carousel-control">›</a>'],
            slideSpeed: 300,
            paginationSpeed: 400,
            items: 3,
            itemsDesktop: [1199, 3],
            itemsDesktopSmall: [979, 2],
            itemsTablet: [768, 2],
            itemsMobile: [479, 1],
            autoPlay: false
          });
        }
      });
    };

    // Wait for DOM to be fully ready
    const timer = setTimeout(initCarousels, 300);
    
    return () => clearTimeout(timer);
  }, [isReady, homeData.banners]);

  async function handleAddCart(productId) {
    if (!isAuthenticated) {
      alert('Please log in to continue.');
      return;
    }

    const result = await addToCart(productId, 1);
    if (!result.success) {
      alert('Failed to add product to cart');
    }
  }

  async function handleAddWishlist(productId) {
    if (!isAuthenticated) {
      alert('Please log in to continue.');
      return;
    }

    const result = await addToWishlist(productId);
    if (!result.success) {
      alert('Failed to add product to wishlist');
    }
  }

  const banners = homeData.banners || {};

  return (
    <>
      <div className="row">
        <HomeSidebar
          categories={categories}
          hotDeals={homeData.hot_deals}
          specialOffers={specialOffers}
          isAuthenticated={isAuthenticated}
          onAddCart={handleAddCart}
        />
        <div className="col-xs-12 col-sm-12 col-md-9 homebanner-holder">
          <Hero banners={banners.header_banners || []} />
          <NewProductsTabs
            categories={categories}
            products={homeData.latest_products}
            isAuthenticated={isAuthenticated}
            onAddCart={handleAddCart}
            onAddWishlist={handleAddWishlist}
          />
          <MiddleBanners banners={banners.middle_banners || []} />
          <FeaturedStrip
            categories={categories}
            products={homeData.latest_products}
            isAuthenticated={isAuthenticated}
            onAddCart={handleAddCart}
            onAddWishlist={handleAddWishlist}
          />
          <WideBanner large={banners.wide_banner_large} small={banners.wide_banner_small} />
          <BlogSlider blogs={homeData.blogs} />
          <section className="section new-arriavls">
            <h3 className="section-title">Featured Products</h3>
            <ProductCarousel
              products={homeData.latest_products}
              isAuthenticated={isAuthenticated}
              onAddCart={handleAddCart}
              onAddWishlist={handleAddWishlist}
              className="owl-carousel home-owl-carousel custom-carousel owl-theme outer-top-xs"
            />
          </section>
        </div>
      </div>
      <BrandsCarousel />
    </>
  );
}
