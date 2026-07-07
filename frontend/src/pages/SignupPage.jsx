import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';

export default function SignupPage() {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [userRoles, setUserRoles] = useState([]);
  const [formData, setFormData] = useState({
    email: '',
    mobile_no: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
    user_role_id: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUserRoles();
  }, []);

  const fetchUserRoles = async () => {
    try {
      const response = await apiClient.get('/roles/');
      setUserRoles(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch user roles:', error);
    }
  };

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
    setErrors({});

    // Validate passwords match
    if (formData.password !== formData.password_confirm) {
      alert('Password and confirm password should be same');
      return;
    }

    setLoading(true);

    const result = await signup(formData);

    if (result.success) {
      alert('Registration successful! Please login.');
      navigate('/login');
    } else {
      setErrors(result.error);
    }
    setLoading(false);
  };

  return (
    <>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
      <link rel="stylesheet" href="/assets/css/style.css" />
      
      <div className="container-fluid">
        <div className='h-100 d-flex align-items-center justify-content-center mt-5'>
          <div className="card" style={{ width: '30%', top: '100px' }}>
            <div className="card-header text-center">
              <h2 style={{ color: '#333' }}>Sign Up</h2>
            </div>
            <div className="card-body m-3 justify-content-center">
              <form onSubmit={handleSubmit}>
                {errors.user_role_id && <span className="text-danger">User Role : {errors.user_role_id}</span>}
                
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
                    <label htmlFor="mobile_no" className="col-form-label">Mobile Number :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="text"
                      id="mobile_no"
                      name="mobile_no"
                      className="form-control"
                      value={formData.mobile_no}
                      onChange={handleChange}
                      required
                    />
                    {errors.mobile_no && <span className="text-danger">{errors.mobile_no}</span>}
                  </div>
                </div>
                
                <div className="row g-3 align-items-center mt-1">
                  <div className="col-4">
                    <label htmlFor="first_name" className="col-form-label">First Name :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="text"
                      id="first_name"
                      name="first_name"
                      className="form-control"
                      value={formData.first_name}
                      onChange={handleChange}
                      required
                    />
                    {errors.first_name && <span className="text-danger">{errors.first_name}</span>}
                  </div>
                </div>
                
                <div className="row g-3 align-items-center mt-1">
                  <div className="col-4">
                    <label htmlFor="last_name" className="col-form-label">Last Name :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="text"
                      id="last_name"
                      name="last_name"
                      className="form-control"
                      value={formData.last_name}
                      onChange={handleChange}
                      required
                    />
                    {errors.last_name && <span className="text-danger">{errors.last_name}</span>}
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
                      pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
                      title="Password must be at least 8 characters, contain at least one uppercase letter, one lowercase letter, one number, and one special character"
                    />
                    {errors.password && <span className="text-danger">{errors.password}</span>}
                  </div>
                </div>
                
                <div className="row g-3 align-items-center my-1">
                  <div className="col-4">
                    <label htmlFor="password_confirm" className="col-form-label">Confirm Password :</label>
                  </div>
                  <div className="col-8">
                    <input
                      type="password"
                      id="password_confirm"
                      name="password_confirm"
                      className="form-control"
                      value={formData.password_confirm}
                      onChange={handleChange}
                      required
                      pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
                      title="Password must be at least 8 characters, contain at least one uppercase letter, one lowercase letter, one number, and one special character"
                    />
                  </div>
                </div>
                
                <div className="row g-3 align-items-center my-1">
                  <div className="col-4">
                    <label htmlFor="user_role_id" className="col-form-label">User Role :</label>
                  </div>
                  <div className="col-sm-8">
                    <select
                      className="form-control"
                      name="user_role_id"
                      value={formData.user_role_id}
                      onChange={handleChange}
                      required
                    >
                      <option value="" disabled>Select Role</option>
                      {userRoles.map((role) => (
                        <option key={role.id} value={role.id}>{role.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                <div style={{ marginBottom: '15px' }} className='my-1'>
                  <button type="submit" className='btn btn-primary sign-btn' disabled={loading}>
                    {loading ? 'Signing up...' : 'Sign Up'}
                  </button>
                </div>
              </form>
              
              <p style={{ fontSize: '12px', color: '#888' }}>
                Already have an account? <Link to="/login">Log in</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </>
  );
}
