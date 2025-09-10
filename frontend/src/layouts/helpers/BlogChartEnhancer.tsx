import React, { useEffect, useState } from "react";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import ChartDisplay from "@/layouts/shortcodes/ChartDisplay";
import type { SupportedChartType } from "@/types/BlogChartTypes";

interface BlogChartEnhancerProps {
  chartType: SupportedChartType;
  chartTitle: string;
  enabled: boolean;
}

const BlogChartEnhancer: React.FC<BlogChartEnhancerProps> = ({
  chartType,
  chartTitle,
  enabled,
}) => {
  const [isChartOpen, setIsChartOpen] = useState(false);
  const [isLargeViewport, setIsLargeViewport] = useState(false);

  useEffect(() => {
    const checkViewport = () => {
      setIsLargeViewport(window.innerWidth >= 1024); // LG breakpoint
    };

    checkViewport();
    window.addEventListener("resize", checkViewport);

    return () => window.removeEventListener("resize", checkViewport);
  }, [enabled]);

  useEffect(() => {
    if (!enabled || !isLargeViewport) {
      return;
    }

    const handleImageClick = (event: Event) => {
      const target = event.target as HTMLElement;

      // Check if clicked element is an image within blog content
      if (target.tagName === "IMG") {
        const contentArea = document.querySelector(".content");
        if (contentArea && contentArea.contains(target)) {
          event.preventDefault();
          event.stopPropagation();
          setIsChartOpen(true);
        }
      }
    };

    // Add click listeners to all images in content area
    const contentImages = document.querySelectorAll(".content img");
    contentImages.forEach((img) => {
      img.addEventListener("click", handleImageClick);
      // Add visual indication that image is clickable on LG+ viewports
      (img as HTMLElement).style.cursor = "pointer";
      (img as HTMLElement).style.transition = "opacity 0.2s";

      img.addEventListener("mouseenter", () => {
        (img as HTMLElement).style.opacity = "0.9";
      });

      img.addEventListener("mouseleave", () => {
        (img as HTMLElement).style.opacity = "1";
      });
    });

    return () => {
      contentImages.forEach((img) => {
        img.removeEventListener("click", handleImageClick);
        (img as HTMLElement).style.cursor = "";
        (img as HTMLElement).style.transition = "";
        (img as HTMLElement).style.opacity = "";
      });
    };
  }, [enabled, isLargeViewport]);

  const CustomLightboxContent = () => (
    <div className="flex h-full w-full items-center justify-center p-8">
      <div className="w-full max-w-6xl">
        <ChartDisplay
          title={chartTitle}
          category="Interactive Analysis"
          description={`Interactive ${chartTitle} chart visualization`}
          chartType={chartType}
          className="chart-lightbox-display"
          titleOnly={false}
        />
      </div>
    </div>
  );

  if (!enabled || !isLargeViewport) {
    return null;
  }

  return (
    <Lightbox
      open={isChartOpen}
      close={() => setIsChartOpen(false)}
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
  );
};

export default BlogChartEnhancer;
