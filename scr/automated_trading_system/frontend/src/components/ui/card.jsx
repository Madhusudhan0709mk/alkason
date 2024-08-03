
import React from 'react';

export const Card = ({ children, className }) => {
  return <div className={`bg-white shadow-md rounded p-4 ${className}`}>{children}</div>;
};

export const CardHeader = ({ children }) => {
  return <h2 className="text-xl font-semibold mb-2">{children}</h2>;
};

export const CardContent = ({ children }) => {
  return <div className="mt-2">{children}</div>;
};
