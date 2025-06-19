import React, { useState } from "react";
import AwesomeLightbox from "react-awesome-lightbox";
import "react-awesome-lightbox/build/style.css";

interface ImageLightboxProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  thumbnailClassName?: string;
  enableLightbox?: boolean;
  images?: Array<{ url: string; title?: string }>;
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

  const lightboxImages = images || [{ url: src, title: alt }];
  const startIndex = images ? images.findIndex((img) => img.url === src) : 0;

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
      {enableLightbox && isOpen && (
        <AwesomeLightbox
          images={lightboxImages}
          startIndex={startIndex}
          onClose={() => setIsOpen(false)}
          allowZoom={true}
          allowRotate={true}
          allowReset={true}
          showTitle={true}
        />
      )}
    </div>
  );
}
