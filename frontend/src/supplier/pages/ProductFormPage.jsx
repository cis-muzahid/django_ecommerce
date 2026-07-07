import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  getProduct,
  createProduct,
  updateProduct,
  getCategories,
} from '../services/productService';

const EMPTY_FORM = {
  name: '',
  description: '',
  price: '',
  weight: '',
  length: '',
  width: '',
  height: '',
  tag: '',
  category: '',
  slug: '',
};

export default function ProductFormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [form, setForm] = useState(EMPTY_FORM);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    loadCategories();
    if (isEdit) {
      loadProduct();
    }
  }, [id]);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data.results || data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const loadProduct = async () => {
    try {
      setLoading(true);
      const data = await getProduct(id);
      setForm({
        name: data.name || '',
        description: data.description || '',
        price: data.price || '',
        weight: data.weight || '',
        length: data.length || '',
        width: data.width || '',
        height: data.height || '',
        tag: data.tag || '',
        category: data.category?.id || data.category || '',
        slug: data.slug || '',
      });
    } catch (err) {
      console.error('Failed to load product:', err);
      setErrors({ general: 'Failed to load product.' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: undefined, general: undefined }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    setSuccessMsg('');

    const fd = new FormData();
    Object.entries(form).forEach(([key, val]) => {
      if (val !== '' && val !== null && val !== undefined) {
        fd.append(key, val);
      }
    });

    try {
      if (isEdit) {
        await updateProduct(id, fd);
      } else {
        await createProduct(fd);
      }
      setSuccessMsg(isEdit ? 'Product updated successfully.' : 'Product created successfully.');
      setTimeout(() => navigate('/supplier/products'), 1000);
    } catch (err) {
      console.error('Failed to save product:', err);
      if (err.response?.data) {
        const apiErrors = err.response.data;
        if (typeof apiErrors === 'object') {
          setErrors(apiErrors);
        } else {
          setErrors({ general: String(apiErrors) });
        }
      } else {
        setErrors({ general: 'An error occurred. Please try again.' });
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <p style={{ margin: 'auto', textAlign: 'center' }}>
          <b>Loading...</b>
        </p>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">
              {isEdit ? 'Edit Product' : 'Add Product'}
            </h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <Link to="/supplier/products" className="btn btn-secondary">
                <i className="fa fa-arrow-left"></i> Back to Products
              </Link>
            </div>
          </div>

          <div className="card-body">
            {successMsg && (
              <div className="alert alert-success">{successMsg}</div>
            )}
            {errors.general && (
              <div className="alert alert-danger">{errors.general}</div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group row">
                <label className="col-sm-4 col-form-label">
                  Product Name <span className="text-danger">*</span>
                </label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="name"
                    className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                    value={form.name}
                    onChange={handleChange}
                    required
                  />
                  {errors.name && (
                    <div className="invalid-feedback">{errors.name}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Description</label>
                <div className="col-sm-8">
                  <textarea
                    name="description"
                    className={`form-control ${errors.description ? 'is-invalid' : ''}`}
                    rows="5"
                    value={form.description}
                    onChange={handleChange}
                  />
                  {errors.description && (
                    <div className="invalid-feedback">{errors.description}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">
                  Price <span className="text-danger">*</span>
                </label>
                <div className="col-sm-8">
                  <input
                    type="number"
                    name="price"
                    className={`form-control ${errors.price ? 'is-invalid' : ''}`}
                    value={form.price}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                    required
                  />
                  {errors.price && (
                    <div className="invalid-feedback">{errors.price}</div>
                  )}
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
                <label className="col-sm-4 col-form-label">Slug</label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="slug"
                    className={`form-control ${errors.slug ? 'is-invalid' : ''}`}
                    value={form.slug}
                    onChange={handleChange}
                    placeholder="auto-generated if empty"
                  />
                  {errors.slug && (
                    <div className="invalid-feedback">{errors.slug}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Tag</label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="tag"
                    className={`form-control ${errors.tag ? 'is-invalid' : ''}`}
                    value={form.tag}
                    onChange={handleChange}
                    placeholder="e.g. new, sale, featured"
                  />
                  {errors.tag && (
                    <div className="invalid-feedback">{errors.tag}</div>
                  )}
                </div>
              </div>

              <hr />
              <h6 className="font-weight-bold mb-3">Dimensions &amp; Weight</h6>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Weight (kg)</label>
                <div className="col-sm-8">
                  <input
                    type="number"
                    name="weight"
                    className={`form-control ${errors.weight ? 'is-invalid' : ''}`}
                    value={form.weight}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                  />
                  {errors.weight && (
                    <div className="invalid-feedback">{errors.weight}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Length (cm)</label>
                <div className="col-sm-8">
                  <input
                    type="number"
                    name="length"
                    className={`form-control ${errors.length ? 'is-invalid' : ''}`}
                    value={form.length}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                  />
                  {errors.length && (
                    <div className="invalid-feedback">{errors.length}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Width (cm)</label>
                <div className="col-sm-8">
                  <input
                    type="number"
                    name="width"
                    className={`form-control ${errors.width ? 'is-invalid' : ''}`}
                    value={form.width}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                  />
                  {errors.width && (
                    <div className="invalid-feedback">{errors.width}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Height (cm)</label>
                <div className="col-sm-8">
                  <input
                    type="number"
                    name="height"
                    className={`form-control ${errors.height ? 'is-invalid' : ''}`}
                    value={form.height}
                    onChange={handleChange}
                    min="0"
                    step="0.01"
                  />
                  {errors.height && (
                    <div className="invalid-feedback">{errors.height}</div>
                  )}
                </div>
              </div>

              <div className="form-group row mt-4">
                <div className="col-sm-8 offset-sm-4">
                  <button type="submit" className="btn btn-primary mr-2" disabled={saving}>
                    {saving ? 'Saving...' : isEdit ? 'Update Product' : 'Add Product'}
                  </button>
                  <Link to="/supplier/products" className="btn btn-secondary">
                    Cancel
                  </Link>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
