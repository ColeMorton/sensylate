import React, { useState, useEffect } from "react";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";

interface ImageLightboxProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  thumbnailClassName?: string;
  enableLightbox?: boolean;
  images?: Array<{ src: string; alt?: string }>;
}

export default function ImageLightbox({
  src,
  alt,
  width,
  height,
  className = "",
  thumbnailClassName = "",
  enableLightbox = true,
  images,
}: ImageLightboxProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkIsMobile();
    window.addEventListener("resize", checkIsMobile);

    return () => window.removeEventListener("resize", checkIsMobile);
  }, []);

  const handleImageClick = () => {
    if (enableLightbox && !isMobile) {
      setIsOpen(true);
    }
  };

  const lightboxImages = images || [{ src: src, alt: alt }];
  const startIndex = images ? images.findIndex((img) => img.src === src) : 0;

  const imageElement = (
    <img
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={`${className} ${thumbnailClassName} ${enableLightbox && !isMobile ? "cursor-pointer transition-opacity hover:opacity-90" : ""}`}
      onClick={handleImageClick}
      onKeyDown={(e) => {
        if (
          enableLightbox &&
          !isMobile &&
          (e.key === "Enter" || e.key === " ")
        ) {
          e.preventDefault();
          setIsOpen(true);
        }
      }}
      tabIndex={enableLightbox && !isMobile ? 0 : -1}
      role={enableLightbox && !isMobile ? "button" : undefined}
      aria-label={
        enableLightbox && !isMobile ? `Open ${alt} in lightbox` : undefined
      }
    />
  );

  return (
    <div>
      {imageElement}
      <Lightbox
        open={enableLightbox && isOpen}
        close={() => setIsOpen(false)}
        slides={lightboxImages}
        index={startIndex}
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
        }}
      />
    </div>
  );
}
