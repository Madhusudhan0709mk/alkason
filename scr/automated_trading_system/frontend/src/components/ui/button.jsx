import React from 'react';
export const Button = ({ children, type }) => {
  return (
    <button type={type} className="btn btn-primary bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
      {children}
    </button>
  );
};
