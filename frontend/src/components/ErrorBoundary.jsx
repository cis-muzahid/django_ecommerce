import { Component } from 'react';
import { Link } from 'react-router-dom';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="container" style={{ paddingTop: '80px', paddingBottom: '80px' }}>
          <div className="row">
            <div className="col-md-8 col-md-offset-2 text-center">
              <div style={{
                background: '#fff',
                borderRadius: '8px',
                padding: '50px 30px',
                boxShadow: '0 2px 20px rgba(0,0,0,0.08)'
              }}>
                <i
                  className="fa fa-exclamation-triangle"
                  style={{ fontSize: '64px', color: '#e74c3c', marginBottom: '20px' }}
                ></i>
                <h2 style={{ marginBottom: '15px', color: '#333' }}>
                  Oops! Something went wrong
                </h2>
                <p className="text-muted" style={{ fontSize: '16px', marginBottom: '30px' }}>
                  We're sorry for the inconvenience. An unexpected error has occurred.
                  Please try refreshing the page or go back to the homepage.
                </p>

                <div>
                  <button
                    onClick={() => window.location.reload()}
                    className="btn btn-primary"
                    style={{ marginRight: '10px', padding: '10px 30px' }}
                  >
                    <i className="fa fa-refresh"></i> Refresh Page
                  </button>
                  <a
                    href="/"
                    className="btn btn-default"
                    style={{ padding: '10px 30px' }}
                  >
                    <i className="fa fa-home"></i> Go to Homepage
                  </a>
                </div>

                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <div style={{
                    marginTop: '30px',
                    textAlign: 'left',
                    background: '#f8f9fa',
                    padding: '15px',
                    borderRadius: '4px',
                    fontSize: '13px',
                    overflow: 'auto'
                  }}>
                    <strong>Error Details (Development Only):</strong>
                    <pre style={{ whiteSpace: 'pre-wrap', color: '#e74c3c' }}>
                      {this.state.error.toString()}
                    </pre>
                    {this.state.errorInfo && (
                      <pre style={{ whiteSpace: 'pre-wrap', color: '#666', fontSize: '12px' }}>
                        {this.state.errorInfo.componentStack}
                      </pre>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
