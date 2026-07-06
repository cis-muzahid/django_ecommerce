import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, requiredRole }) {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check role if required
  if (requiredRole) {
    const userRole = user?.user_role?.name;
    
    if (requiredRole === 'supplier' && userRole !== 'supplier') {
      return <Navigate to="/" replace />;
    }
    
    if (requiredRole === 'admin' && !user?.is_superuser) {
      return <Navigate to="/" replace />;
    }
  }

  return children;
}
