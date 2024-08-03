// src/components/ui/input.js

import React from 'react';

export const Input = ({ id, name, type, value, onChange, step }) => {
  return (
    <input
      id={id}
      name={name}
      type={type}
      step={step}
      value={value}
      onChange={onChange}
      className="border p-2 rounded w-full"
    />
  );
};
