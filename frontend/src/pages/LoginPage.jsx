import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error for this field
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    const result = await login(formData.email, formData.password);

    if (result.success) {
      // Redirect based on user role
      navigate(result.redirectPath || '/');
    } else {
      setErrors({ general: result.error });
    }
    setLoading(false);
  };

  return (
    <>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
      <link rel="stylesheet" href="/assets/css/style.css" />
      
      <div className="container-fluid">
        {errors.general && (
          <div className="container mt-5">
            <div className="alert alert-danger">{errors.general}</div>
          </div>
        )}
        
        <div className='h-100 d-flex align-items-center justify-content-center mt-5'>
          <div className="card" style={{ width: '30%', top: '100px' }}>
            <div className="card-header text-center">
              <h2 style={{ color: '#333' }}>Login</h2>
            </div>
            <div className="card-body m-3 justify-content-center">
              <form onSubmit={handleSubmit}>
                <div className="row g-3 align-items-center mt-1">
                  <div className="col-4">
                    <label htmlFor="email" className="col-form-label">Email :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="email"
                      id="email"
                      name="email"
                      className="form-control"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                    {errors.email && <span className="text-danger">{errors.email}</span>}
                  </div>
                </div>
                
                <div className="row g-3 align-items-center my-1">
                  <div className="col-4">
                    <label htmlFor="password" className="col-form-label">Password :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="password"
                      id="password"
                      name="password"
                      className="form-control"
                      value={formData.password}
                      onChange={handleChange}
                      required
                    />
                    {errors.password && <span className="text-danger">{errors.password}</span>}
                  </div>
                </div>
                
                <div style={{ marginBottom: '15px' }} className='my-1'>
                  <button type="submit" className='btn btn-primary sign-btn' disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                  </button>
                </div>
              </form>
              
              <p style={{ fontSize: '12px', color: '#888' }}>
                Don't have an account? <Link to="/signup">Sign up</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </>
  );
}
