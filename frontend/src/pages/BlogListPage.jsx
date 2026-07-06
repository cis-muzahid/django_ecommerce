import { useEffect, useState } from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom';
import BlogSidebar from '../components/BlogSidebar';
import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';
import apiClient from '../services/apiClient';
import { stripHtml } from '../utils/catalog';

function blogHref(blog) {
  return `/user/blog/${blog.id}`;
}

function blogImage(blog) {
  return blog.image_url || blog.image || '/assets/images/blog-post/post1.jpg';
}

function authorName(blog) {
  const name = `${blog.user?.first_name || ''} ${blog.user?.last_name || ''}`.trim();
  return name || blog.user?.username || 'Default Admin';
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

function excerpt(blog, length = 120) {
  const value = stripHtml(blog.excerpt || blog.description || '');
  return value.length > length
    ? `${value.slice(0, length)}...`
    : value;
}

function BlogSummary({ blog, compact = false }) {
  return (
    <div className={`blog-post ${compact ? 'inner-bottom-30' : ''}`}>
      <Link to={blogHref(blog)}>
        <img
          className="img-responsive center-block"
          src={blogImage(blog)}
          alt={blog.title}
        />
      </Link>

      {compact ? (
        <h4>
          <Link to={blogHref(blog)}>
            {blog.title}
          </Link>
        </h4>
      ) : (
        <>
          <h1>
            <Link to={blogHref(blog)}>
              {blog.title}
            </Link>
          </h1>

          <span className="author">
            {authorName(blog)}
          </span>

          <span className="review">
            {blog.comment_count || 0} Comments
          </span>

          <span className="date-time">
            {formatDate(blog.created_at)}
          </span>

          <p>{excerpt(blog)}</p>

          <Link
            to={blogHref(blog)}
            className="btn btn-primary read-more"
          >
            READ MORE
          </Link>
        </>
      )}
    </div>
  );
}

export default function BlogListPage() {
  const { categoryId } = useParams();
  const [searchParams] = useSearchParams();

  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const [selectedCategory, setSelectedCategory] =
    useState(categoryId || '');

  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');

  useEffect(() => {
    setSearchQuery(searchParams.get('search') || '');
    setSelectedCategory(categoryId || '');
  }, [categoryId, searchParams]);

  useEffect(() => {
    fetchBlogs(searchQuery);
  }, [selectedCategory, searchQuery]);

  async function fetchBlogs(query = searchQuery) {
    try {
      setLoading(true);

      const params = {};

      if (selectedCategory) {
        params.category = selectedCategory;
      }

      if (query) {
        params.search = query;
      }

      const res =
        await apiClient.get('/blogs/', {
          params
        });

      setBlogs(
        res.data.results || res.data || []
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'Blogs' }]} />

      <div className="row">
        <div className="blog-page react-blog-page">
          <div className="col-xs-12 col-sm-9 col-md-9 rht-col blog-main">
            {loading ? (
              <div className="blog-empty">
                <p className="text-center">Loading...</p>
              </div>
            ) : blogs.length ? (
              blogs.map((blog) => (
                <div key={blog.id}>
                  <BlogSummary blog={blog} />
                  <hr />
                </div>
              ))
            ) : (
              <div className="blog-empty">
                <p className="text-center">No Data Found</p>
              </div>
            )}
          </div>

          <BlogSidebar onSearch={(query) => setSearchQuery(query)} />
        </div>
      </div>

      <BrandsCarousel />
    </>
  );
}
