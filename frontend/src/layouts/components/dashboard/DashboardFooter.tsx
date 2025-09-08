/**
 * Dynamic Dashboard Footer Component
 * 
 * Renders dashboard footers based on configuration instead of hardcoded logic.
 * Part of the configuration-driven PhotoBooth system.
 */

import React from 'react';
import type { DashboardFooterConfig } from '@/types/DashboardLayoutTypes';

interface DashboardFooterProps {
  config: DashboardFooterConfig;
  mode?: 'light' | 'dark';
}

const DashboardFooter: React.FC<DashboardFooterProps> = ({ 
  config, 
  mode = 'light' 
}) => {
  if (!config.enabled) {
    return null;
  }

  const baseClasses = 'dashboard-footer flex justify-center';
  const textClasses = 'brand-text text-text-dark dark:text-darkmode-text-dark m-0 mb-8 text-4xl font-semibold';
  const containerClasses = config.className ? `${baseClasses} ${config.className}` : baseClasses;

  return (
    <div className={containerClasses}>
      <h1 className={textClasses}>
        {config.text}
      </h1>
    </div>
  );
};

export default DashboardFooter;