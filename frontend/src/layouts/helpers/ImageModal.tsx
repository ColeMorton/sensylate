import React, { useEffect, useRef } from "react";
import { useFeatureFlag } from "@/hooks/useFeatureFlag";

export interface ImageModalProps {
  isOpen: boolean;
  onClose: () => void;
  imageSrc: string;
  imageAlt: string;
  imageSrcSet?: string;
}

const ImageModal: React.FC<ImageModalProps> = ({
  isOpen,
  onClose,
  imageSrc,
  imageAlt,
  imageSrcSet,
}) => {
  const isImageExpandEnabled = useFeatureFlag("image_expand");
  const modalRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  // Handle keyboard events
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      // Prevent body scroll when modal is open
      document.body.style.overflow = "hidden";

      // Focus management
      modalRef.current?.focus();
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [isOpen, onClose]);

  // Click outside to close
  const handleOverlayClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  // Don't render if feature is disabled or modal is closed
  if (!isImageExpandEnabled || !isOpen) {
    return null;
  }

  return (
    <div
      ref={modalRef}
      className="image-modal fixed inset-0 z-[9999] flex items-center justify-center p-4"
      onClick={handleOverlayClick}
      tabIndex={-1}
      role="dialog"
      aria-modal="true"
      aria-label="Expanded image view"
    >
      {/* Overlay */}
      <div className="image-modal-overlay absolute inset-0 bg-black/80 transition-opacity duration-300" />

      {/* Modal Content */}
      <div className="image-modal-content relative z-10 max-h-full max-w-full">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute -top-12 right-0 z-20 rounded-full bg-black/50 p-2 text-white hover:bg-black/70 focus:bg-black/70 focus:ring-2 focus:ring-white/50 focus:outline-none sm:top-0 sm:-right-12"
          aria-label="Close image"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {/* Image */}
        <img
          ref={imageRef}
          src={imageSrc}
          srcSet={imageSrcSet}
          alt={imageAlt}
          className="max-h-[90vh] max-w-[90vw] object-contain transition-all duration-300 ease-out"
          style={{
            animation: isOpen ? "imageModalFadeIn 0.3s ease-out" : undefined,
          }}
        />
      </div>
    </div>
  );
};

export default ImageModal;
