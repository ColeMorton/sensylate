import React from "react";

interface LogoDisplayProps {
  size?: "small" | "medium" | "large" | "xl";
  className?: string;
  showBackground?: boolean;
}

const LogoDisplay: React.FC<LogoDisplayProps> = ({
  size = "medium",
  className = "",
  showBackground = false,
}) => {
  const getSizeClasses = () => {
    switch (size) {
      case "small":
        return "text-xl md:text-2xl";
      case "medium":
        return "text-3xl md:text-4xl";
      case "large":
        return "text-5xl md:text-6xl";
      case "xl":
        return "text-7xl md:text-8xl lg:text-9xl";
      default:
        return "text-3xl md:text-4xl";
    }
  };

  const backgroundClasses = showBackground
    ? "bg-body dark:bg-darkmode-body p-6 rounded-lg shadow-sm"
    : "bg-transparent";

  return (
    <div className={`logo-display-container ${backgroundClasses} ${className}`}>
      <h1
        className={`brand-text text-text-dark dark:text-darkmode-text-dark m-0 font-semibold ${getSizeClasses()}`}
      >
        Cole Morton
      </h1>
    </div>
  );
};

export default LogoDisplay;
