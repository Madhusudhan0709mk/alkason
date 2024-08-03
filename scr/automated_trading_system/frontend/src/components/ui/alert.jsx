import React from 'react';

export const Alert = ({ children, variant }) => {
  const variantStyles = variant === 'destructive' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800';
  return <div className={`p-4 rounded ${variantStyles}`}>{children}</div>;
};

export const AlertDescription = ({ children }) => {
  return <p>{children}</p>;
};
