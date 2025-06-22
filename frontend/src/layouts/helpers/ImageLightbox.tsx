import React, { useState } from "react";
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

  const handleImageClick = () => {
    if (enableLightbox) {
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
      className={`${thumbnailClassName} ${enableLightbox ? "cursor-pointer transition-opacity hover:opacity-90" : ""}`}
      onClick={handleImageClick}
      onKeyDown={(e) => {
        if (enableLightbox && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          setIsOpen(true);
        }
      }}
      tabIndex={enableLightbox ? 0 : -1}
      role={enableLightbox ? "button" : undefined}
      aria-label={enableLightbox ? `Open ${alt} in lightbox` : undefined}
    />
  );

  return (
    <div className={className}>
      {imageElement}
      <Lightbox
        open={enableLightbox && isOpen}
        close={() => setIsOpen(false)}
        slides={lightboxImages}
        index={startIndex}
      />
    </div>
  );
}
