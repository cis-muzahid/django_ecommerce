import { useEffect, useRef, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  getProduct,
  getProductAttributes,
  createProductAttribute,
  updateProductAttribute,
  deleteProductAttribute,
  getProductSpecifications,
  createProductSpecification,
  updateProductSpecification,
  deleteProductSpecification,
} from '../services/productService';

// ─── Attribute Modal ────────────────────────────────────────────────────────
function AttributeModal({ productId, attr, onSaved, onClose }) {
  const [form, setForm] = useState({
    title: attr?.title || '',
    value: attr?.value || '',
    out_of_stoke: attr?.out_of_stoke || false,
    product_image: null,
  });
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});
  const fileRef = useRef();

  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;
    if (type === 'file') {
      setForm((p) => ({ ...p, product_image: files[0] }));
    } else if (type === 'checkbox') {
      setForm((p) => ({ ...p, [name]: checked }));
    } else {
      setForm((p) => ({ ...p, [name]: value }));
    }
    setErrors((p) => ({ ...p, [name]: undefined }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    const fd = new FormData();
    fd.append('title', form.title);
    fd.append('value', form.value);
    fd.append('out_of_stoke', form.out_of_stoke ? 'true' : 'false');
    if (form.product_image) {
      fd.append('product_image', form.product_image);
    }
    try {
      if (attr?.id) {
        await updateProductAttribute(productId, attr.id, fd);
      } else {
        await createProductAttribute(productId, fd);
      }
      onSaved();
    } catch (err) {
      console.error('Failed to save attribute:', err);
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
            <h5 className="modal-title">{attr?.id ? 'Edit Attribute' : 'Add Attribute'}</h5>
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
                <label className="col-sm-4 col-form-label">
                  Value <span className="text-danger">*</span>
                </label>
                <div className="col-sm-8">
                  <input
                    type="text"
                    name="value"
                    className={`form-control ${errors.value ? 'is-invalid' : ''}`}
                    value={form.value}
                    onChange={handleChange}
                    required
                  />
                  {errors.value && <div className="invalid-feedback">{errors.value}</div>}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Product Image</label>
                <div className="col-sm-8">
                  {attr?.product_image && !form.product_image && (
                    <div className="mb-1">
                      <img
                        src={attr.product_image}
                        alt="current"
                        style={{ width: '80px', height: '60px', objectFit: 'cover' }}
                      />
                      <small className="text-muted ml-2">Current image</small>
                    </div>
                  )}
                  <input
                    type="file"
                    name="product_image"
                    className="form-control-file"
                    accept="image/*"
                    ref={fileRef}
                    onChange={handleChange}
                  />
                  {errors.product_image && (
                    <div className="text-danger small">{errors.product_image}</div>
                  )}
                </div>
              </div>

              <div className="form-group row">
                <label className="col-sm-4 col-form-label">Out of Stock</label>
                <div className="col-sm-8 d-flex align-items-center">
                  <div className="custom-control custom-checkbox">
                    <input
                      type="checkbox"
                      className="custom-control-input"
                      id="outOfStock"
                      name="out_of_stoke"
                      checked={form.out_of_stoke}
                      onChange={handleChange}
                    />
                    <label className="custom-control-label" htmlFor="outOfStock">
                      Mark as out of stock
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Saving...' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

// ─── Specification Modal ─────────────────────────────────────────────────────
function SpecificationModal({ productId, spec, onSaved, onClose }) {
  const [form, setForm] = useState({
    title: spec?.title || '',
    description: spec?.description || '',
  });
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((p) => ({ ...p, [name]: value }));
    setErrors((p) => ({ ...p, [name]: undefined }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    try {
      if (spec?.id) {
        await updateProductSpecification(productId, spec.id, form);
      } else {
        await createProductSpecification(productId, form);
      }
      onSaved();
    } catch (err) {
      console.error('Failed to save specification:', err);
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
            <h5 className="modal-title">{spec?.id ? 'Edit Specification' : 'Add Specification'}</h5>
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
                <label className="col-sm-4 col-form-label">
                  Description <span className="text-danger">*</span>
                </label>
                <div className="col-sm-8">
                  <textarea
                    name="description"
                    className={`form-control ${errors.description ? 'is-invalid' : ''}`}
                    rows="4"
                    value={form.description}
                    onChange={handleChange}
                    required
                  />
                  {errors.description && (
                    <div className="invalid-feedback">{errors.description}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? 'Saving...' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

// ─── Main ProductDetailPage ──────────────────────────────────────────────────
export default function ProductDetailPage() {
  const { id } = useParams();

  const [product, setProduct] = useState(null);
  const [attributes, setAttributes] = useState([]);
  const [specifications, setSpecifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Attribute modal state
  const [attrModal, setAttrModal] = useState(null); // null | 'add' | {attr object}
  // Specification modal state
  const [specModal, setSpecModal] = useState(null); // null | 'add' | {spec object}

  useEffect(() => {
    loadAll();
  }, [id]);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [prod, attrs, specs] = await Promise.all([
        getProduct(id),
        getProductAttributes(id),
        getProductSpecifications(id),
      ]);
      setProduct(prod);
      setAttributes(attrs.results || attrs);
      setSpecifications(specs.results || specs);
    } catch (err) {
      console.error('Failed to load product detail:', err);
      setErrorMsg('Failed to load product details.');
    } finally {
      setLoading(false);
    }
  };

  const reloadAttributes = async () => {
    try {
      const data = await getProductAttributes(id);
      setAttributes(data.results || data);
    } catch (err) {
      console.error('Failed to reload attributes:', err);
    }
  };

  const reloadSpecifications = async () => {
    try {
      const data = await getProductSpecifications(id);
      setSpecifications(data.results || data);
    } catch (err) {
      console.error('Failed to reload specifications:', err);
    }
  };

  const handleDeleteAttribute = async (attrId) => {
    if (!confirm('Delete this attribute?')) return;
    try {
      await deleteProductAttribute(id, attrId);
      setSuccessMsg('Attribute deleted.');
      reloadAttributes();
    } catch (err) {
      setErrorMsg('Failed to delete attribute.');
    }
  };

  const handleDeleteSpecification = async (specId) => {
    if (!confirm('Delete this specification?')) return;
    try {
      await deleteProductSpecification(id, specId);
      setSuccessMsg('Specification deleted.');
      reloadSpecifications();
    } catch (err) {
      setErrorMsg('Failed to delete specification.');
    }
  };

  const onAttrSaved = () => {
    setAttrModal(null);
    setSuccessMsg('Attribute saved successfully.');
    reloadAttributes();
  };

  const onSpecSaved = () => {
    setSpecModal(null);
    setSuccessMsg('Specification saved successfully.');
    reloadSpecifications();
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

  if (!product) {
    return (
      <div className="container">
        <div className="alert alert-danger">{errorMsg || 'Product not found.'}</div>
        <Link to="/supplier/products" className="btn btn-secondary">
          &larr; Back to Products
        </Link>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Modals */}
      {attrModal !== null && (
        <AttributeModal
          productId={id}
          attr={attrModal === 'add' ? null : attrModal}
          onSaved={onAttrSaved}
          onClose={() => setAttrModal(null)}
        />
      )}
      {specModal !== null && (
        <SpecificationModal
          productId={id}
          spec={specModal === 'add' ? null : specModal}
          onSaved={onSpecSaved}
          onClose={() => setSpecModal(null)}
        />
      )}

      {/* Product Info Card */}
      <div className="row categorie_main">
        <div className="col-12 card mb-4">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">
              Product: {product.name}
            </h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <Link
                to={`/supplier/products/${id}/edit`}
                className="btn btn-info mr-2"
              >
                <i className="fa fa-pencil"></i> Edit Product
              </Link>
              <Link to="/supplier/products" className="btn btn-secondary">
                <i className="fa fa-arrow-left"></i> Back
              </Link>
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
            <table className="table table-bordered table-sm" style={{ maxWidth: '600px' }}>
              <tbody>
                <tr>
                  <th>Name</th>
                  <td>{product.name}</td>
                </tr>
                <tr>
                  <th>Price</th>
                  <td>₹{parseFloat(product.price || 0).toFixed(2)}</td>
                </tr>
                <tr>
                  <th>Category</th>
                  <td>{product.category?.name || product.category || 'N/A'}</td>
                </tr>
                <tr>
                  <th>Slug</th>
                  <td>{product.slug || 'N/A'}</td>
                </tr>
                <tr>
                  <th>Tag</th>
                  <td>{product.tag || 'N/A'}</td>
                </tr>
                <tr>
                  <th>Weight</th>
                  <td>{product.weight ? `${product.weight} kg` : 'N/A'}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Attributes Card */}
        <div className="col-12 card mb-4">
          <div className="card-header">
            <h5 className="card-title font-weight-bold mt-1">Product Attributes</h5>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <button
                className="btn btn-info btn-sm"
                onClick={() => setAttrModal('add')}
              >
                <i className="fa fa-plus"></i> Add Attribute
              </button>
            </div>
          </div>
          <div className="card-body">
            {attributes.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th>#</th>
                    <th>Image</th>
                    <th>Title</th>
                    <th>Value</th>
                    <th>Out of Stock</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {attributes.map((attr, idx) => (
                    <tr key={attr.id} className="text-center">
                      <td>{idx + 1}</td>
                      <td>
                        {attr.product_image ? (
                          <img
                            src={attr.product_image}
                            alt={attr.title}
                            style={{ width: '60px', height: '50px', objectFit: 'cover' }}
                          />
                        ) : (
                          <span className="text-muted">—</span>
                        )}
                      </td>
                      <td>{attr.title}</td>
                      <td>{attr.value}</td>
                      <td>
                        {attr.out_of_stoke ? (
                          <span className="badge badge-danger">Yes</span>
                        ) : (
                          <span className="badge badge-success">No</span>
                        )}
                      </td>
                      <td>
                        <span className="ml-2 mr-2">
                          <a
                            href="#"
                            onClick={(e) => {
                              e.preventDefault();
                              setAttrModal(attr);
                            }}
                          >
                            <i className="fa fa-pencil text-success"></i>
                          </a>
                        </span>
                        <span className="ml-2 mr-2">
                          <a
                            href="#"
                            onClick={(e) => {
                              e.preventDefault();
                              handleDeleteAttribute(attr.id);
                            }}
                          >
                            <i className="fa fa-trash text-danger"></i>
                          </a>
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-center text-muted">
                No attributes found. Click "Add Attribute" to add one.
              </p>
            )}
          </div>
        </div>

        {/* Specifications Card */}
        <div className="col-12 card mb-4">
          <div className="card-header">
            <h5 className="card-title font-weight-bold mt-1">Product Specifications</h5>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <button
                className="btn btn-info btn-sm"
                onClick={() => setSpecModal('add')}
              >
                <i className="fa fa-plus"></i> Add Specification
              </button>
            </div>
          </div>
          <div className="card-body">
            {specifications.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th>#</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {specifications.map((spec, idx) => (
                    <tr key={spec.id} className="text-center">
                      <td>{idx + 1}</td>
                      <td>{spec.title}</td>
                      <td style={{ maxWidth: '400px', textAlign: 'left' }}>
                        {spec.description}
                      </td>
                      <td>
                        <span className="ml-2 mr-2">
                          <a
                            href="#"
                            onClick={(e) => {
                              e.preventDefault();
                              setSpecModal(spec);
                            }}
                          >
                            <i className="fa fa-pencil text-success"></i>
                          </a>
                        </span>
                        <span className="ml-2 mr-2">
                          <a
                            href="#"
                            onClick={(e) => {
                              e.preventDefault();
                              handleDeleteSpecification(spec.id);
                            }}
                          >
                            <i className="fa fa-trash text-danger"></i>
                          </a>
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-center text-muted">
                No specifications found. Click "Add Specification" to add one.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
