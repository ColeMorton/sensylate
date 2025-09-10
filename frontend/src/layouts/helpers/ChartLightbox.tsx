import React, { useState, useEffect } from "react";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import ChartDisplay from "@/layouts/shortcodes/ChartDisplay";
import type { ChartLightboxProps } from "@/types/BlogChartTypes";

const ChartLightbox: React.FC<ChartLightboxProps> = ({
  src,
  alt,
  width,
  height,
  className = "",
  thumbnailClassName = "",
  chartType,
  chartTitle,
  viewportThreshold = 1024, // LG breakpoint default
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLargeViewport, setIsLargeViewport] = useState(false);

  useEffect(() => {
    const checkViewport = () => {
      setIsLargeViewport(window.innerWidth >= viewportThreshold);
    };

    checkViewport();
    window.addEventListener("resize", checkViewport);

    return () => window.removeEventListener("resize", checkViewport);
  }, [viewportThreshold]);

  const handleImageClick = () => {
    if (isLargeViewport) {
      setIsOpen(true);
    }
  };

  const thumbnailImage = (
    <img
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={`${className} ${thumbnailClassName} ${
        isLargeViewport
          ? "cursor-pointer transition-opacity hover:opacity-90"
          : ""
      }`}
      onClick={handleImageClick}
      onKeyDown={(e) => {
        if (isLargeViewport && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          setIsOpen(true);
        }
      }}
      tabIndex={isLargeViewport ? 0 : -1}
      role={isLargeViewport ? "button" : undefined}
      aria-label={isLargeViewport ? `Open ${alt} chart in lightbox` : undefined}
    />
  );

  const CustomLightboxContent = () => (
    <div className="flex h-full w-full items-center justify-center p-8">
      <div className="w-full max-w-6xl">
        <ChartDisplay
          title={chartTitle || `${chartType} Chart`}
          category="Interactive Chart"
          description={`Interactive ${chartType} chart visualization`}
          chartType={chartType}
          className="chart-lightbox-display"
          titleOnly={false}
        />
      </div>
    </div>
  );

  return (
    <div>
      {thumbnailImage}
      {isLargeViewport && (
        <Lightbox
          open={isOpen}
          close={() => setIsOpen(false)}
          slides={[{ src: "" }]} // Required by library, but we override content
          toolbar={{
            buttons: ["close"],
          }}
          controller={{
            closeOnBackdropClick: true,
            closeOnPullDown: true,
            closeOnPullUp: true,
          }}
          carousel={{
            finite: true,
            preload: 0,
          }}
          render={{
            buttonPrev: () => null,
            buttonNext: () => null,
            slide: () => <CustomLightboxContent />,
          }}
          styles={{
            container: {
              backgroundColor: "rgba(0, 0, 0, 0.9)",
            },
          }}
        />
      )}
    </div>
  );
};

export default ChartLightbox;
