import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLayout } from '../context/LayoutContext';
import apiClient from '../services/apiClient';
import { categoryHref, stripHtml } from '../utils/catalog';

function blogHref(blog) {
  return `/user/blog/${blog.id}`;
}

function blogImage(blog) {
  return blog.image_url || blog.image || '/assets/images/blog-post/post1.jpg';
}

function formatDate(value) {
  if (!value) return '';

  return new Date(value).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

function excerpt(blog, length = 105) {
  const value = stripHtml(blog.excerpt || blog.description || '');
  return value.length > length ? `${value.slice(0, length)}...` : value;
}

function flattenCategories(categories, result = []) {
  categories.forEach((category) => {
    result.push(category);
    flattenCategories(category.subcategories || category.children || [], result);
  });

  return result;
}

function CompactBlog({ blog }) {
  return (
    <div className="blog-post inner-bottom-30">
      <Link to={blogHref(blog)}>
        <img className="img-responsive" src={blogImage(blog)} alt={blog.title} />
      </Link>
      <h4>
        <Link to={blogHref(blog)}>{blog.title}</Link>
      </h4>
      <span className="review">{blog.comment_count || 0} Comments</span>
      <span className="date-time">{formatDate(blog.created_at)}</span>
      <p>{excerpt(blog)}</p>
    </div>
  );
}

export default function BlogSidebar({ onSearch }) {
  const navigate = useNavigate();
  const { categories } = useLayout();
  const [searchQuery, setSearchQuery] = useState('');
  const [blogCategories, setBlogCategories] = useState([]);
  const [allBlogs, setAllBlogs] = useState([]);
  const [activeTab, setActiveTab] = useState('popular');

  useEffect(() => {
    fetchSidebarData();
  }, []);

  async function fetchSidebarData() {
    try {
      const [categoryResponse, blogResponse] = await Promise.all([
        apiClient.get('/blog-categories/'),
        apiClient.get('/blogs/'),
      ]);

      setBlogCategories(categoryResponse.data.results || categoryResponse.data || []);
      setAllBlogs(blogResponse.data.results || blogResponse.data || []);
    } catch (error) {
      console.error('Failed to fetch blog sidebar data:', error);
    }
  }

  function handleSearch(event) {
    event.preventDefault();
    const query = searchQuery.trim();

    if (onSearch) {
      onSearch(query);
      return;
    }

    navigate(query ? `/user/blogs?search=${encodeURIComponent(query)}` : '/user/blogs');
  }

  const recentBlogs = useMemo(
    () => [...allBlogs].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 2),
    [allBlogs],
  );

  const popularBlogs = useMemo(
    () => [...allBlogs].sort((a, b) => (b.comment_count || 0) - (a.comment_count || 0)).slice(0, 2),
    [allBlogs],
  );

  const sidebarBlogs = activeTab === 'popular' ? popularBlogs : recentBlogs;
  const productCategories = useMemo(() => flattenCategories(categories, []), [categories]);

  return (
    <div className="col-xs-12 col-sm-3 col-md-3 sidebar blog-sidebar">
      <div className="sidebar-module-container">
        <div className="search-area outer-bottom-small">
          <form id="search-form" onSubmit={handleSearch}>
            <div className="control-group">
              <input
                className="search-field"
                name="q"
                placeholder="Type to search"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
            </div>
          </form>
        </div>

        <div className="sidebar-widget blog-category-widget outer-bottom-xs">
          <h3 className="section-title">Category</h3>
          <div className="sidebar-widget-body m-t-10">
            <div className="accordion">
              {blogCategories.length ? (
                <ul className="blog-sidebar-list">
                  {blogCategories.map((category) => (
                    <li key={category.id}>
                      <Link className="item" to={`/user/blogs/${category.id}`}>
                        {category.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-center">No Data Found</p>
              )}
            </div>
          </div>
        </div>

        <div className="sidebar-widget outer-bottom-xs">
          <h3 className="section-title">Tab Widget</h3>
          <ul className="nav nav-tabs">
            <li className={activeTab === 'popular' ? 'active' : ''}>
              <a
                href="#popular"
                data-toggle="tab"
                onClick={(event) => {
                  event.preventDefault();
                  setActiveTab('popular');
                }}
              >
                popular post
              </a>
            </li>
            <li className={activeTab === 'recent' ? 'active' : ''}>
              <a
                href="#recent"
                data-toggle="tab"
                onClick={(event) => {
                  event.preventDefault();
                  setActiveTab('recent');
                }}
              >
                recent post
              </a>
            </li>
          </ul>
          <div className="tab-content">
            <div className="tab-pane active m-t-20">
              {sidebarBlogs.length ? (
                sidebarBlogs.map((blog) => <CompactBlog blog={blog} key={blog.id} />)
              ) : (
                <p className="text-center">No Data Found</p>
              )}
            </div>
          </div>
        </div>

        <div className="sidebar-widget product-tag">
          <h3 className="section-title">Product Tags</h3>
          <div className="sidebar-widget-body outer-top-xs">
            <div className="tag-list">
              {productCategories.length ? (
                productCategories.map((category) => (
                  <Link className="item" title={category.name} to={categoryHref(category)} key={category.id}>
                    {category.name}
                  </Link>
                ))
              ) : (
                <p className="text-center">No Data Found</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
