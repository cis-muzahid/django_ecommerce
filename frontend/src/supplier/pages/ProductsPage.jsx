import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProducts, deleteProduct } from '../services/productService';

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchProducts();
  }, [currentPage, searchQuery]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const data = await getProducts(currentPage, searchQuery);
      setProducts(data.results || data);
      setTotalPages(data.total_pages || 1);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchProducts();
  };

  const handleDelete = async (productId) => {
    if (!confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await deleteProduct(productId);
      fetchProducts();
    } catch (error) {
      console.error('Failed to delete product:', error);
      alert('Failed to delete product');
    }
  };

  return (
    <div className="container">
      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">Products</h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <form onSubmit={handleSearch} className="d-flex mr-4">
                <input
                  name="q"
                  className="form-control me-2 mr-4"
                  type="search"
                  placeholder="Search"
                  aria-label="Search"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button className="btn btn-outline-info" type="submit">
                  Search
                </button>
              </form>
              <Link to="/supplier/products/add" className="btn btn-info me-md-2 mr-5" type="button">
                Add Product
              </Link>
            </div>
          </div>

          <div className="card-body">
            {loading ? (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>Loading...</b>
              </p>
            ) : products.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th scope="col">S. no.</th>
                    <th scope="col">Product</th>
                    <th scope="col">Product Slug</th>
                    <th scope="col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((product, index) => (
                    <tr key={product.id} className="text-center">
                      <th scope="row">{(currentPage - 1) * 10 + index + 1}</th>
                      <td>
                        <Link to={`/supplier/products/${product.id}`}>
                          {product.name}
                        </Link>
                      </td>
                      <td>{product.slug}</td>
                      <td>
                        <div className="d-flex justify-content-center">
                          <span className="ml-2 mr-2">
                            <Link
                              to={`/supplier/products/${product.id}/edit`}
                              style={{ fontWeight: 100, color: 'black' }}
                            >
                              <i className="fa fa-pencil text-success"></i>
                            </Link>
                          </span>
                          <span className="ml-2 mr-2">
                            <a
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                handleDelete(product.id);
                              }}
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
                <li key={i + 1} className="page-item">
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
