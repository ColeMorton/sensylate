import React, { useEffect, useState } from "react";

interface PinnedCardsHandlerProps {
  show: boolean;
  hide?: boolean;
  onHidden?: () => void;
  containerId?: string;
}

const PinnedCardsHandler: React.FC<PinnedCardsHandlerProps> = ({
  show,
  hide = false,
  onHidden,
  containerId = "pinned-cards-container",
}) => {
  const [isVisible, setIsVisible] = useState(false);

  // Handle showing cards
  useEffect(() => {
    if (show && !hide) {
      const timer = setTimeout(() => {
        const container = document.getElementById(containerId);
        if (container) {
          container.classList.add("visible");
          setIsVisible(true);
        }
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [show, hide, containerId]);

  // Handle hiding cards
  useEffect(() => {
    if (hide && isVisible) {
      const container = document.getElementById(containerId);
      if (container) {
        container.classList.remove("visible");
        setIsVisible(false);

        // Wait for animation to complete before calling onHidden
        const timer = setTimeout(() => {
          if (onHidden) {
            onHidden();
          }
        }, 800); // Match the CSS transition duration

        return () => clearTimeout(timer);
      }
    }
  }, [hide, isVisible, onHidden, containerId]);

  return null;
};

export default PinnedCardsHandler;
