import { useEffect, useRef, useState } from 'react';
import {
  getBanners,
  getBanner,
  createBanner,
  updateBanner,
  deleteBanner,
  getCategories,
} from '../services/bannerService';

const BANNER_TYPES = [
  { value: 'header_banner', label: 'Header Banner' },
  { value: 'middle_banner', label: 'Middle Banner' },
  { value: 'wide_banner_large', label: 'Wide Banner Large' },
  { value: 'wide_banner_small', label: 'Wide Banner Small' },
];

const EMPTY_FORM = {
  title: '',
  subtitle: '',
  description: '',
  type: '',
  category: '',
  image: null,
};

// ─── Banner Modal ────────────────────────────────────────────────────────────
function BannerModal({ banner, categories, onSaved, onClose }) {
  const isEdit = Boolean(banner?.id);
  const [form, setForm] = useState(
    isEdit
      ? {
          title: banner.title || '',
          subtitle: banner.subtitle || '',
          description: banner.description || '',
          type: banner.type || '',
          category: banner.category?.id || banner.category || '',
          image: null,
        }
      : { ...EMPTY_FORM }
  );
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});
  const fileRef = useRef();

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      setForm((p) => ({ ...p, image: files[0] }));
    } else {
      setForm((p) => ({ ...p, [name]: value }));
    }
    setErrors((p) => ({ ...p, [name]: undefined, general: undefined }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    const fd = new FormData();
    fd.append('title', form.title);
    if (form.subtitle) fd.append('subtitle', form.subtitle);
    if (form.description) fd.append('description', form.description);
    if (form.type) fd.append('type', form.type);
    if (form.category) fd.append('category', form.category);
    if (form.image) fd.append('image', form.image);

    try {
      if (isEdit) {
        await updateBanner(banner.id, fd);
      } else {
        await createBanner(fd);
      }
      onSaved();
    } catch (err) {
      console.error('Failed to save banner:', err);
      if (err.response?.data && typeof err.response.data === 'object') {
        setErrors(err.response.data);
      } else {
        setErrors({ general: 'An error occurred. Please try again.' });
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      className="modal fade show"
      style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}
      tabIndex="-1"
    >
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{isEdit ? 'Edit Banner' : 'Add Banner'}</h5>
            <button type="button" className="close" onClick={onClose}>
              <span>&times;</span>
            </button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              {errors.general && (
                <div className="alert alert-danger">{errors.general}</div>
              )}

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">
                  Title <span className="text-danger">*</span>
                </label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="title"
                    className={`form-control ${errors.title ? 'is-invalid' : ''}`}
                    value={form.title}
                    onChange={handleChange}
                    required
                  />
                  {errors.title && <div className="invalid-feedback">{errors.title}</div>}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Subtitle</label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="subtitle"
                    className={`form-control ${errors.subtitle ? 'is-invalid' : ''}`}
                    value={form.subtitle}
                    onChange={handleChange}
                  />
                  {errors.subtitle && (
                    <div className="invalid-feedback">{errors.subtitle}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Description</label>
                <div className="col-sm-8">
                  <textarea
                    name="description"
                    className={`form-control ${errors.description ? 'is-invalid' : ''}`}
                    rows="3"
                    value={form.description}
                    onChange={handleChange}
                  />
                  {errors.description && (
                    <div className="invalid-feedback">{errors.description}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Type</label>
                <div className="col-sm-8">
                  <select
                    name="type"
                    className={`form-control ${errors.type ? 'is-invalid' : ''}`}
                    value={form.type}
                    onChange={handleChange}
                  >
                    <option value="">-- Select Type --</option>
                    {BANNER_TYPES.map((t) => (
                      <option key={t.value} value={t.value}>
                        {t.label}
                      </option>
                    ))}
                  </select>
                  {errors.type && <div className="invalid-feedback">{errors.type}</div>}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Category</label>
                <div className="col-sm-8">
                  <select
                    name="category"
                    className={`form-control ${errors.category ? 'is-invalid' : ''}`}
                    value={form.category}
                    onChange={handleChange}
                  >
                    <option value="">-- Select Category --</option>
                    {categories.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name}
                      </option>
                    ))}
                  </select>
                  {errors.category && (
                    <div className="invalid-feedback">{errors.category}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">
                  Image {!isEdit && <span className="text-danger">*</span>}
                </label>
                <div className="col-sm-8">
                  {isEdit && banner.image && !form.image && (
                    <div className="mb-2">
                      <img
                        src={banner.image}
                        alt={banner.title}
                        style={{ width: '120px', height: '60px', objectFit: 'cover' }}
                      />
                      <small className="text-muted ml-2">Current image (leave blank to keep)</small>
                    </div>
                  )}
                  <input
                    type="file"
                    name="image"
                    className="form-control-file"
                    accept="image/*"
                    ref={fileRef}
                    onChange={handleChange}
                    required={!isEdit}
                  />
                  {errors.image && (
                    <div className="text-danger small">{errors.image}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Saving...' : isEdit ? 'Update Banner' : 'Add Banner'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

// ─── BannersPage ─────────────────────────────────────────────────────────────
export default function BannersPage() {
  const [banners, setBanners] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [modal, setModal] = useState(null); // null | 'add' | {banner object}
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    fetchBanners();
    loadCategories();
  }, [currentPage]);

  const fetchBanners = async () => {
    try {
      setLoading(true);
      const data = await getBanners(currentPage);
      setBanners(data.results || data);
      if (data.count) {
        setTotalPages(Math.ceil(data.count / 10));
      } else {
        setTotalPages(data.total_pages || 1);
      }
    } catch (error) {
      console.error('Failed to fetch banners:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data.results || data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const handleDelete = async (bannerId) => {
    if (!confirm('Are you sure you want to delete this banner?')) return;
    try {
      await deleteBanner(bannerId);
      setSuccessMsg('Banner deleted successfully.');
      fetchBanners();
    } catch (error) {
      console.error('Failed to delete banner:', error);
      setErrorMsg('Failed to delete banner.');
    }
  };

  const onSaved = () => {
    setModal(null);
    setSuccessMsg('Banner saved successfully.');
    fetchBanners();
  };

  return (
    <div className="container">
      {modal !== null && (
        <BannerModal
          banner={modal === 'add' ? null : modal}
          categories={categories}
          onSaved={onSaved}
          onClose={() => setModal(null)}
        />
      )}

      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">Banners</h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <button
                className="btn btn-info mr-5"
                type="button"
                onClick={() => setModal('add')}
              >
                <i className="fa fa-plus"></i> Add Banner
              </button>
            </div>
          </div>

          <div className="card-body">
            {successMsg && (
              <div className="alert alert-success alert-dismissible">
                <button type="button" className="close" onClick={() => setSuccessMsg('')}>
                  <span>&times;</span>
                </button>
                {successMsg}
              </div>
            )}
            {errorMsg && (
              <div className="alert alert-danger alert-dismissible">
                <button type="button" className="close" onClick={() => setErrorMsg('')}>
                  <span>&times;</span>
                </button>
                {errorMsg}
              </div>
            )}

            {loading ? (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>Loading...</b>
              </p>
            ) : banners.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th scope="col">S. no.</th>
                    <th scope="col">Image</th>
                    <th scope="col">Title</th>
                    <th scope="col">Subtitle</th>
                    <th scope="col">Type</th>
                    <th scope="col">Category</th>
                    <th scope="col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {banners.map((banner, index) => (
                    <tr key={banner.id} className="text-center">
                      <th scope="row">{(currentPage - 1) * 10 + index + 1}</th>
                      <td>
                        {banner.image ? (
                          <img
                            src={banner.image}
                            alt={banner.title}
                            style={{ width: '100px', height: '50px', objectFit: 'cover' }}
                          />
                        ) : (
                          <span className="text-muted">No image</span>
                        )}
                      </td>
                      <td>{banner.title}</td>
                      <td>{banner.subtitle || '—'}</td>
                      <td>
                        {BANNER_TYPES.find((t) => t.value === banner.type)?.label ||
                          banner.type ||
                          '—'}
                      </td>
                      <td>{banner.category?.name || '—'}</td>
                      <td>
                        <div className="d-flex justify-content-center">
                          <span className="ml-2 mr-2">
                            <a
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                setModal(banner);
                              }}
                              title="Edit"
                            >
                              <i className="fa fa-pencil text-success"></i>
                            </a>
                          </span>
                          <span className="ml-2 mr-2">
                            <a
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                handleDelete(banner.id);
                              }}
                              title="Delete"
                            >
                              <i className="fa fa-trash text-danger"></i>
                            </a>
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>No Data Found</b>
              </p>
            )}
          </div>

          <hr />

          <div className="card-footer clearfix bg-white justify-content-md-start">
            <ul className="pagination pagination-sm m-0 float-right">
              {currentPage > 1 && (
                <li className="page-item">
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(currentPage - 1);
                    }}
                  >
                    &laquo;
                  </a>
                </li>
              )}
              {[...Array(totalPages)].map((_, i) => (
                <li
                  key={i + 1}
                  className={`page-item ${currentPage === i + 1 ? 'active' : ''}`}
                >
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(i + 1);
                    }}
                  >
                    {i + 1}
                  </a>
                </li>
              ))}
              {currentPage < totalPages && (
                <li className="page-item">
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(currentPage + 1);
                    }}
                  >
                    &raquo;
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
