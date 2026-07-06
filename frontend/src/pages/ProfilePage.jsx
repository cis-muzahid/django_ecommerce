import { useEffect, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';

function userDisplayName(user) {
  const name = `${user?.first_name || ''} ${user?.last_name || ''}`.trim();
  return name || user?.username || user?.email || 'Customer';
}

function userInitials(user) {
  const name = userDisplayName(user);
  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0])
    .join('')
    .toUpperCase();
}

export default function ProfilePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, user, loading: authLoading, refreshUserProfile } = useAuth();
  const photoInputRef = useRef(null);
  const [addresses, setAddresses] = useState([]);
  const [showEditProfileModal, setShowEditProfileModal] = useState(false);
  const [showAddAddressModal, setShowAddAddressModal] = useState(false);
  const [showEditAddressModal, setShowEditAddressModal] = useState(false);
  const [editingAddress, setEditingAddress] = useState(null);
  const [photoUploading, setPhotoUploading] = useState(false);
  const [profileForm, setProfileForm] = useState({
    username: '',
    first_name: '',
    last_name: '',
    mobile_no: ''
  });
  const [addressForm, setAddressForm] = useState({
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    is_default: false
  });

  useEffect(() => {
    if (authLoading) {
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    fetchAddresses();
    if (user) {
      setProfileForm({
        username: user.username || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        mobile_no: user.mobile_no || ''
      });
    }
  }, [authLoading, isAuthenticated, user]);


  const fetchAddresses = async () => {
    try {
      const response = await apiClient.get('/addresses/');
      setAddresses(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch addresses:', error);
    }
  };

  const handleProfileFormChange = (e) => {
    setProfileForm({
      ...profileForm,
      [e.target.name]: e.target.value
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.put('/auth/profile/', profileForm);
      await refreshUserProfile();
      alert('Profile updated successfully!');
      setShowEditProfileModal(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile');
    }
  };

  const handlePhotoUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append('profile_image', file);

    try {
      setPhotoUploading(true);
      await apiClient.put('/auth/profile/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      await refreshUserProfile();
      alert('Profile photo updated successfully!');
    } catch (error) {
      console.error('Failed to upload profile photo:', error);
      alert('Failed to upload profile photo');
    } finally {
      setPhotoUploading(false);
      e.target.value = '';
    }
  };

  const handleRemovePhoto = async () => {
    if (!user?.profile_image_url) {
      return;
    }

    if (!confirm('Remove your profile photo?')) {
      return;
    }

    try {
      setPhotoUploading(true);
      await apiClient.put('/auth/profile/', { remove_profile_image: true });
      await refreshUserProfile();
      alert('Profile photo removed successfully!');
    } catch (error) {
      console.error('Failed to remove profile photo:', error);
      alert('Failed to remove profile photo');
    } finally {
      setPhotoUploading(false);
    }
  };

  const handleAddressFormChange = (e) => {
    const value = e.target.type === 'radio' ? e.target.value === 'True' : e.target.value;
    setAddressForm({
      ...addressForm,
      [e.target.name]: value
    });
  };

  const handleAddressSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingAddress) {
        await apiClient.put(`/addresses/${editingAddress.id}/`, addressForm);
        alert('Address updated successfully!');
        setShowEditAddressModal(false);
      } else {
        await apiClient.post('/addresses/', addressForm);
        alert('Address added successfully!');
        setShowAddAddressModal(false);
      }
      setEditingAddress(null);
      setAddressForm({
        street: '',
        city: '',
        state: '',
        postal_code: '',
        country: '',
        is_default: false
      });
      fetchAddresses();
    } catch (error) {
      console.error('Failed to save address:', error);
      alert('Failed to save address');
    }
  };

  const handleEditAddress = (address) => {
    setEditingAddress(address);
    setAddressForm({
      street: address.street,
      city: address.city,
      state: address.state,
      postal_code: address.postal_code,
      country: address.country,
      is_default: address.is_default
    });
    setShowEditAddressModal(true);
  };

  const handleDeleteAddress = async (addressId) => {
    if (confirm('Are you sure you want to delete this address?')) {
      try {
        await apiClient.delete(`/addresses/${addressId}/`);
        alert('Address deleted successfully!');
        fetchAddresses();
      } catch (error) {
        console.error('Failed to delete address:', error);
        alert('Failed to delete address');
      }
    }
  };

  if (authLoading) {
    return <p className="text-center" style={{ padding: '50px' }}>Loading profile...</p>;
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'My Profile' }]} />
      <div className="profile-page profile-dashboard-page">
        <div className="row">
          <div className="col-xs-12 col-sm-9 col-md-9 profile-main">
            <div className="profile-hero">
              <div className="profile-avatar-panel">
                <div className="profile-avatar">
                  {user?.profile_image_url ? (
                    <img src={user.profile_image_url} alt={userDisplayName(user)} />
                  ) : (
                    <span>{userInitials(user)}</span>
                  )}
                </div>
                <div className="profile-avatar-actions">
                  <h2>{userDisplayName(user)}</h2>
                  <p>{user?.email}</p>
                  <div className="profile-avatar-buttons">
                    <input
                      ref={photoInputRef}
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={handlePhotoUpload}
                    />
                    <button
                      type="button"
                      className="btn btn-primary profile-action-btn"
                      onClick={() => photoInputRef.current?.click()}
                      disabled={photoUploading}
                    >
                      {photoUploading ? 'Uploading...' : 'Upload Photo'}
                    </button>
                    <button
                      type="button"
                      className="btn btn-default profile-action-btn"
                      onClick={handleRemovePhoto}
                      disabled={photoUploading || !user?.profile_image_url}
                    >
                      Remove Photo
                    </button>
                  </div>
                </div>
              </div>

              <div className="profile-summary-grid">
                <div className="profile-summary-item">
                  <span className="label">Username</span>
                  <strong>{user?.username || '-'}</strong>
                </div>
                <div className="profile-summary-item">
                  <span className="label">First Name</span>
                  <strong>{user?.first_name || '-'}</strong>
                </div>
                <div className="profile-summary-item">
                  <span className="label">Last Name</span>
                  <strong>{user?.last_name || '-'}</strong>
                </div>
                <div className="profile-summary-item">
                  <span className="label">Mobile</span>
                  <strong>{user?.mobile_no || '-'}</strong>
                </div>
                <div className="profile-summary-item profile-summary-wide">
                  <span className="label">Email</span>
                  <strong>{user?.email || '-'}</strong>
                </div>
              </div>
            </div>

            <div className="profile-section">
              <div className="profile-section-header">
                <h3>Addresses</h3>
                {addresses.length < 5 && (
                  <button
                    type="button"
                    onClick={() => setShowAddAddressModal(true)}
                    className="btn btn-info profile-action-btn"
                    id="add_new_address_btn"
                  >
                    Add New Address
                  </button>
                )}
              </div>

              <div className="profile-address-list">
                {addresses.length > 0 ? (
                  addresses.map((address) => (
                    <div key={address.id} className="profile-address-card">
                      <div>
                        <div className="profile-address-title">
                          {address.is_default && <span className="default-pill">Default</span>}
                          <strong>{address.street}</strong>
                        </div>
                        <p>{address.city}, {address.state}</p>
                        <p>{address.postal_code}, {address.country}</p>
                      </div>
                      <div className="profile-address-actions">
                        <button
                          type="button"
                          className="btn btn-link profile-icon-btn"
                          onClick={() => handleEditAddress(address)}
                          aria-label="Edit address"
                        >
                          <i className="fa fa-pencil text-success"></i>
                        </button>
                        <button
                          type="button"
                          className="btn btn-link profile-icon-btn"
                          onClick={() => handleDeleteAddress(address.id)}
                          aria-label="Delete address"
                        >
                          <i className="fa fa-trash text-danger"></i>
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="profile-empty-state">No saved addresses yet.</div>
                )}
              </div>
            </div>
          </div>

          <div className="col-xs-12 col-sm-3 col-md-3 sidebar profile-sidebar">
            <div className="profile-progress-card">
              <h4>My Progress</h4>
              <ul className="nav nav-checkout-progress list-unstyled">
                <li>
                  <button
                    type="button"
                    onClick={() => setShowEditProfileModal(true)}
                    className="btn-link profile-progress-link"
                  >
                    Edit Profile
                  </button>
                </li>
                <li>
                  <Link className={location.pathname.includes('/orders') ? 'active' : ''} to="/orders">
                    My Orders
                  </Link>
                </li>
                <li>
                  <Link className={location.pathname.includes('/wishlist') ? 'active' : ''} to="/wishlist">
                    My Wishlist
                  </Link>
                </li>
                <li>
                  <Link className={location.pathname.includes('/user_review') ? 'active' : ''} to="/user_review">
                    Reviews
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <BrandsCarousel />

      {/* Edit Profile Modal */}
      {showEditProfileModal && (
        <div className="modal fade in" style={{ display: 'block' }} tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h4 className="modal-title text-center">Update Your Profile</h4>
              </div>
              <form onSubmit={handleProfileSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label className="info-title" htmlFor="username">
                      Username <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="username"
                      name="username"
                      value={profileForm.username}
                      onChange={handleProfileFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="first_name">
                      First Name <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="first_name"
                      name="first_name"
                      value={profileForm.first_name}
                      onChange={handleProfileFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="last_name">
                      Last Name <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="last_name"
                      name="last_name"
                      value={profileForm.last_name}
                      onChange={handleProfileFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="mobile_number">
                      Mobile Number <span>*</span>
                    </label>
                    <input
                      type="number"
                      className="form-control unicase-form-control text-input"
                      id="mobile_number"
                      name="mobile_no"
                      value={profileForm.mobile_no}
                      onChange={handleProfileFormChange}
                      required
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowEditProfileModal(false)}>
                    Close
                  </button>
                  <button type="submit" className="btn btn-success">
                    Update
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Address Modal */}
      {showAddAddressModal && (
        <div className="modal fade in" style={{ display: 'block' }} tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h4 className="modal-title text-center">Add New Address</h4>
              </div>
              <form onSubmit={handleAddressSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <h4 className="checkout-subtitle">Add New Address</h4>
                    <label className="info-title" htmlFor="street">
                      Street <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="street"
                      name="street"
                      value={addressForm.street}
                      onChange={handleAddressFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="city">
                      City <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="city"
                      name="city"
                      value={addressForm.city}
                      onChange={handleAddressFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="state">
                      State <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="state"
                      name="state"
                      value={addressForm.state}
                      onChange={handleAddressFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="postal_code">
                      Postal Code <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="postal_code"
                      name="postal_code"
                      value={addressForm.postal_code}
                      onChange={handleAddressFormChange}
                      required
                    />
                    <label className="info-title" htmlFor="country">
                      Country <span>*</span>
                    </label>
                    <input
                      type="text"
                      className="form-control unicase-form-control text-input"
                      id="country"
                      name="country"
                      value={addressForm.country}
                      onChange={handleAddressFormChange}
                      required
                    />
                    <label>Do you want to add this address as default address?</label>
                    <br />
                    Yes<input type="radio" name="is_default" value="True" onChange={handleAddressFormChange} required />
                    No<input type="radio" name="is_default" value="False" onChange={handleAddressFormChange} />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowAddAddressModal(false)}>
                    Close
                  </button>
                  <button type="submit" className="btn btn-success">
                    Add Address
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Edit Address Modal */}
      {showEditAddressModal && (
        <div className="modal fade in" style={{ display: 'block' }} tabIndex="-1" role="dialog">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h4 className="modal-title text-center">Update Your Address</h4>
              </div>
              <form onSubmit={handleAddressSubmit}>
                <div className="modal-body">
                  <label className="info-title" htmlFor="street">
                    Street <span>*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="street"
                    name="street"
                    value={addressForm.street}
                    onChange={handleAddressFormChange}
                    required
                  />
                  <label className="info-title" htmlFor="city">
                    City <span>*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="city"
                    name="city"
                    value={addressForm.city}
                    onChange={handleAddressFormChange}
                    required
                  />
                  <label className="info-title" htmlFor="state">
                    State <span>*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="state"
                    name="state"
                    value={addressForm.state}
                    onChange={handleAddressFormChange}
                    required
                  />
                  <label className="info-title" htmlFor="postal_code">
                    Postal Code <span>*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="postal_code"
                    name="postal_code"
                    value={addressForm.postal_code}
                    onChange={handleAddressFormChange}
                    required
                  />
                  <label className="info-title" htmlFor="country">
                    Country <span>*</span>
                  </label>
                  <input
                    type="text"
                    className="form-control unicase-form-control text-input"
                    id="country"
                    name="country"
                    value={addressForm.country}
                    onChange={handleAddressFormChange}
                    required
                  />
                  <label>Do you want to add this address as default address?</label>
                  <br />
                  Yes<input type="radio" name="is_default" value="True" checked={addressForm.is_default === true} onChange={handleAddressFormChange} required />
                  No<input type="radio" name="is_default" value="False" checked={addressForm.is_default === false} onChange={handleAddressFormChange} />
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowEditAddressModal(false)}>
                    Close
                  </button>
                  <button type="submit" className="btn btn-success">
                    Update
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {showEditProfileModal || showAddAddressModal || showEditAddressModal ? (
        <div className="modal-backdrop fade in"></div>
      ) : null}

    </>
  );
}
