/**
 * Dynamic Dashboard Header Component
 * 
 * Renders dashboard headers based on configuration instead of hardcoded logic.
 * Part of the configuration-driven PhotoBooth system.
 */

import React from 'react';
import type { DashboardHeaderConfig } from '@/types/DashboardLayoutTypes';

interface DashboardHeaderProps {
  config: DashboardHeaderConfig;
  mode?: 'light' | 'dark';
}

const DashboardHeader: React.FC<DashboardHeaderProps> = ({ 
  config, 
  mode = 'light' 
}) => {
  if (!config.enabled) {
    return null;
  }

  const baseClasses = 'dashboard-header text-center';
  const titleClasses = 'text-dark mt-8 text-4xl font-bold dark:text-white';
  const containerClasses = config.className ? `${baseClasses} ${config.className}` : baseClasses;

  return (
    <div className={containerClasses}>
      <h1 className={titleClasses}>
        {config.title}
      </h1>
    </div>
  );
};

export default DashboardHeader;