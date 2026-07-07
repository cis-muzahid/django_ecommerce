import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import BlogSidebar from '../components/BlogSidebar';
import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';

function authorName(comment) {
  return comment.user_name ||
    `${comment.user?.first_name || ''} ${comment.user?.last_name || ''}`.trim() ||
    comment.user?.username ||
    comment.user?.email ||
    'Default Admin';
}

function timeAgo(value) {
  if (!value) return '';

  const seconds = Math.max(0, Math.floor((Date.now() - new Date(value).getTime()) / 1000));
  const units = [
    ['year', 31536000],
    ['month', 2592000],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
  ];

  for (const [label, size] of units) {
    const amount = Math.floor(seconds / size);
    if (amount >= 1) {
      return `${amount} ${label}${amount > 1 ? 's' : ''}`;
    }
  }

  return 'just now';
}

export default function BlogDetailPage() {
  const { id, slug } = useParams();
  const { isAuthenticated, user } = useAuth();

  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [commentText, setCommentText] = useState('');
  const [replyTextByComment, setReplyTextByComment] = useState({});
  const [editTextByComment, setEditTextByComment] = useState({});
  const [openReplyForm, setOpenReplyForm] = useState(null);
  const [openEditForm, setOpenEditForm] = useState(null);
  const [openReplies, setOpenReplies] = useState({});
  const [commentError, setCommentError] = useState('');
  const [submittingComment, setSubmittingComment] = useState(false);

  useEffect(() => {
    fetchBlog();
  }, [id, slug]);

  async function fetchBlog() {
    try {
      setLoading(true);
      const response = await apiClient.get(id ? `/blogs/${id}/` : `/blogs/slug/${slug}/`);
      setBlog(response.data);
    } catch (error) {
      console.error('Failed to fetch blog:', error);
      setBlog(null);
    } finally {
      setLoading(false);
    }
  }

  function isOwnComment(comment) {
    return Boolean(user?.id && comment.user?.id && user.id === comment.user.id);
  }

  async function submitComment(event) {
    event.preventDefault();
    const description = commentText.trim();

    if (!description) {
      setCommentError('Please enter your comment.');
      return;
    }

    await saveComment({ description });
    setCommentText('');
  }

  async function submitReply(event, commentId) {
    event.preventDefault();
    const description = (replyTextByComment[commentId] || '').trim();

    if (!description) {
      setCommentError('Please enter your reply.');
      return;
    }

    await saveComment({ description, parent_comment: commentId });
    setReplyTextByComment((previous) => ({ ...previous, [commentId]: '' }));
    setOpenReplyForm(null);
    setOpenReplies((previous) => ({ ...previous, [commentId]: true }));
  }

  async function saveComment(payload) {
    try {
      setSubmittingComment(true);
      setCommentError('');
      await apiClient.post(`/blogs/${blog.id}/comments/`, payload);
      await fetchBlog();
    } catch (error) {
      setCommentError(error.response?.data?.detail || 'Unable to save comment. Please login and try again.');
    } finally {
      setSubmittingComment(false);
    }
  }

  async function submitEdit(event, comment) {
    event.preventDefault();
    const description = (editTextByComment[comment.id] || '').trim();

    if (!description) {
      setCommentError('Please enter your comment.');
      return;
    }

    try {
      setSubmittingComment(true);
      setCommentError('');
      await apiClient.patch(`/blogs/${blog.id}/comments/${comment.id}/`, { description });
      setOpenEditForm(null);
      await fetchBlog();
    } catch (error) {
      setCommentError(error.response?.data?.detail || 'Unable to update comment.');
    } finally {
      setSubmittingComment(false);
    }
  }

  async function deleteComment(commentId) {
    try {
      setSubmittingComment(true);
      setCommentError('');
      await apiClient.delete(`/blogs/${blog.id}/comments/${commentId}/`);
      await fetchBlog();
    } catch (error) {
      setCommentError(error.response?.data?.detail || 'Unable to delete comment.');
    } finally {
      setSubmittingComment(false);
    }
  }

  function renderComment(comment, isReply = false) {
    const replies = comment.replies || [];
    const replyFormOpen = openReplyForm === comment.id;
    const editFormOpen = openEditForm === comment.id;
    const repliesOpen = openReplies[comment.id];

    return (
      <div className="row blog-comment-row" key={comment.id}>
        <div className="col-md-2 col-sm-2">
          <img
            src="/assets/images/testimonials/member1.png"
            alt="Comment author"
            className="img-rounded img-responsive"
          />
        </div>
        <div className="col-md-10 col-sm-10 blog-comments outer-bottom-xs">
          <div className="blog-comments inner-bottom-xs">
            <h4
              role="button"
              tabIndex="0"
              onClick={() => {
                if (replies.length) {
                  setOpenReplies((previous) => ({ ...previous, [comment.id]: !previous[comment.id] }));
                }
              }}
              onKeyDown={(event) => {
                if ((event.key === 'Enter' || event.key === ' ') && replies.length) {
                  event.preventDefault();
                  setOpenReplies((previous) => ({ ...previous, [comment.id]: !previous[comment.id] }));
                }
              }}
            >
              {authorName(comment)}
            </h4>
            <span className="review-action pull-right">
              {timeAgo(comment.created_at)} ago
              {isAuthenticated && (
                <>
                  {isOwnComment(comment) && (
                    <>
                      {' / '}
                      <button
                        type="button"
                        className="btn-link"
                        onClick={() => {
                          setOpenEditForm(editFormOpen ? null : comment.id);
                          setEditTextByComment((previous) => ({
                            ...previous,
                            [comment.id]: previous[comment.id] ?? comment.description,
                          }));
                        }}
                      >
                        Repost
                      </button>
                    </>
                  )}
                  {!isReply && (
                    <>
                      {' / '}
                      <button
                        type="button"
                        className="btn-link"
                        onClick={() => setOpenReplyForm(replyFormOpen ? null : comment.id)}
                      >
                        Reply
                      </button>
                    </>
                  )}
                  {isOwnComment(comment) && (
                    <>
                      {' / '}
                      <button
                        type="button"
                        className="btn-link"
                        disabled={submittingComment}
                        onClick={() => deleteComment(comment.id)}
                      >
                        Delete
                      </button>
                    </>
                  )}
                </>
              )}
            </span>
            <p>{comment.description}</p>
          </div>

          {editFormOpen && (
            <form className="register-form blog-inline-comment-form" onSubmit={(event) => submitEdit(event, comment)}>
              <div className="form-group">
                <label className="info-title" htmlFor={`edit-comment-${comment.id}`}>
                  Repost Your {isReply ? 'Reply' : 'Comment'} <span>*</span>
                </label>
                <textarea
                  className="form-control unicase-form-control"
                  id={`edit-comment-${comment.id}`}
                  value={editTextByComment[comment.id] || ''}
                  onChange={(event) => setEditTextByComment((previous) => ({
                    ...previous,
                    [comment.id]: event.target.value,
                  }))}
                  required
                />
              </div>
              <button type="submit" className="btn-upper btn btn-primary checkout-page-button" disabled={submittingComment}>
                Submit Reply
              </button>
            </form>
          )}

          {replyFormOpen && (
            <form className="register-form blog-inline-comment-form" onSubmit={(event) => submitReply(event, comment.id)}>
              <div className="form-group">
                <label className="info-title" htmlFor={`reply-comment-${comment.id}`}>
                  Add Your Reply <span>*</span>
                </label>
                <textarea
                  className="form-control unicase-form-control"
                  id={`reply-comment-${comment.id}`}
                  value={replyTextByComment[comment.id] || ''}
                  onChange={(event) => setReplyTextByComment((previous) => ({
                    ...previous,
                    [comment.id]: event.target.value,
                  }))}
                  required
                />
              </div>
              <button type="submit" className="btn-upper btn btn-primary checkout-page-button" disabled={submittingComment}>
                Submit Reply
              </button>
            </form>
          )}

          {!isReply && replies.length > 0 && repliesOpen && (
            <div className="blog-comments-responce outer-top-xs">
              {replies.map((reply) => renderComment(reply, true))}
            </div>
          )}
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container">
        <p className="text-center">Loading...</p>
      </div>
    );
  }

  if (!blog) {
    return (
      <div className="container">
        <p className="text-center">Blog not found</p>
      </div>
    );
  }

  return (
    <>
      <Breadcrumbs
        items={[
          { label: 'Blogs', link: '/user/blogs' },
          { label: blog.title }
        ]}
      />

      <div className="row">
        <div className="blog-page react-blog-page">
          <div className="col-xs-12 col-sm-9 col-md-9 rht-col blog-main">
            <div className="blog-post">
              <div className="col-lg-12">
                <img
                  className="img-responsive center-block"
                  src={
                    blog.image_url ||
                    blog.image ||
                    '/assets/images/blog-post/post1.jpg'
                  }
                  alt={blog.title}
                />
              </div>

              <h1>{blog.title}</h1>
              <span className="author">
                {`${blog.user?.first_name || ''} ${blog.user?.last_name || ''}`.trim() || blog.user?.username || 'Default Admin'}
              </span>
              <span className="review">{blog.comment_count || 0} Comments</span>
              <span className="date-time">
                {new Date(blog.created_at).toLocaleString()}
              </span>

              <div
                dangerouslySetInnerHTML={{
                  __html: blog.description || ''
                }}
              />

              <div className="social-media">
                <span>share post:</span>
                <a href="#"><i className="fa fa-facebook"></i></a>
                <a href="#"><i className="fa fa-twitter"></i></a>
                <a href="#"><i className="fa fa-linkedin"></i></a>
                <a href="#"><i className="fa fa-rss"></i></a>
                <a href="#" className="hidden-xs"><i className="fa fa-pinterest"></i></a>
              </div>
            </div>

            <div className="blog-review">
              <div className="row">
                <div className="col-md-12">
                  <h3 className="title-review-comments">{blog.comment_count || 0} comments</h3>
                </div>
                {(blog.comments || []).map((comment) => renderComment(comment))}
              </div>
            </div>

            {isAuthenticated && (
              <div className="blog-write-comment outer-bottom-xs outer-top-xs">
                <div className="row">
                  <div className="col-md-12">
                    <h4>Leave A Comment</h4>
                  </div>
                  <form className="register-form" role="form" onSubmit={submitComment}>
                    <div className="col-md-12">
                      <div className="form-group">
                        <label className="info-title" htmlFor="blog-comment">
                          Your Comments <span>*</span>
                        </label>
                        <textarea
                          className="form-control unicase-form-control"
                          id="blog-comment"
                          rows="4"
                          value={commentText}
                          onChange={(event) => setCommentText(event.target.value)}
                          required
                        ></textarea>
                      </div>
                    </div>
                    <div className="col-md-12 outer-bottom-small m-t-20">
                      <button
                        type="submit"
                        className="btn-upper btn btn-primary checkout-page-button"
                        disabled={submittingComment}
                      >
                        Submit Comment
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            {commentError && <p className="text-danger blog-comment-error">{commentError}</p>}
          </div>

          <BlogSidebar />
        </div>
      </div>

      <BrandsCarousel />
    </>
  );
}
