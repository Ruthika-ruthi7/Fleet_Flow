import React from 'react';

const LoadingSpinner = ({ size = 'medium', text = 'Loading...', fullScreen = true }) => {
  const sizeClasses = {
    small: 'h-4 w-4',
    medium: 'h-8 w-8',
    large: 'h-12 w-12',
  };

  const content = (
    <div className="text-center">
      <div className="flex justify-center">
        <div className={`loading-spinner ${sizeClasses[size]}`}></div>
      </div>
      {text && (
        <p className="mt-2 text-sm text-gray-600">{text}</p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        {content}
      </div>
    );
  }

  return content;
};

export default LoadingSpinner;
