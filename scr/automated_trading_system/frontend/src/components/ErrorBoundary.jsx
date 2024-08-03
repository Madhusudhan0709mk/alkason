import React, { useState } from 'react';

const ErrorBoundary = ({ children }) => {
  const [errorState, setErrorState] = useState({ hasError: false, error: null, errorInfo: null });

  const logError = (error, errorInfo) => {
    console.error("Uncaught error:", error, errorInfo);
    
  };

  if (errorState.hasError) {
    return (
      <div className="error-boundary">
        <h1>Something went wrong.</h1>
        <details style={{ whiteSpace: 'pre-wrap' }}>
          {errorState.error && errorState.error.toString()}
          <br />
          {errorState.errorInfo && errorState.errorInfo.componentStack}
        </details>
      </div>
    );
  }

  return children;
};

export default ErrorBoundary;
