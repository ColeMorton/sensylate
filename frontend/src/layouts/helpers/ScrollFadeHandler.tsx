import React, { useEffect, useRef } from "react";

interface ScrollFadeHandlerProps {
  galaxyId: string;
  textId: string;
  fadeDistance?: number;
}

const ScrollFadeHandler: React.FC<ScrollFadeHandlerProps> = ({
  galaxyId,
  textId,
  fadeDistance = 800,
}) => {
  const animationFrameRef = useRef<number>();
  const isThrottledRef = useRef(false);
  const scrollProgressRef = useRef(0);

  useEffect(() => {
    const galaxyElement = document.getElementById(galaxyId);
    const textElement = document.getElementById(textId);

    if (!galaxyElement) {
      throw new Error(
        `ScrollFadeHandler: Element with ID "${galaxyId}" not found`,
      );
    }
    if (!textElement) {
      throw new Error(
        `ScrollFadeHandler: Element with ID "${textId}" not found`,
      );
    }

    const handleWheel = (event: WheelEvent) => {
      // Calculate text opacity (fades twice as fast)
      const textOpacity = Math.max(
        0,
        1 - (scrollProgressRef.current * 2) / fadeDistance,
      );

      // Stop scrolling when text is fully faded (scroll limit reached)
      if (textOpacity <= 0 && event.deltaY > 0) {
        return;
      }

      // Prevent default scrolling behavior
      event.preventDefault();

      if (isThrottledRef.current) {
        return;
      }

      isThrottledRef.current = true;
      animationFrameRef.current = requestAnimationFrame(() => {
        // Accumulate scroll progress based on wheel delta
        scrollProgressRef.current += event.deltaY;

        // Clamp scroll progress to bounds (limit at fadeDistance/2 when text reaches 0)
        const maxProgress = fadeDistance / 2;
        scrollProgressRef.current = Math.max(
          0,
          Math.min(maxProgress, scrollProgressRef.current),
        );

        // Calculate text opacity (fades twice as fast, reaches 0 at 50% progress)
        const newTextOpacity = Math.max(
          0,
          1 - (scrollProgressRef.current * 2) / fadeDistance,
        );

        // Calculate galaxy opacity (fades normally, reaches 0.5 at 100% progress)
        const galaxyOpacity = Math.max(
          0.5,
          1 - scrollProgressRef.current / (fadeDistance / 2),
        );

        textElement.style.opacity = newTextOpacity.toString();
        galaxyElement.style.opacity = galaxyOpacity.toString();

        isThrottledRef.current = false;
      });
    };

    // Set initial opacities
    textElement.style.opacity = "1";
    galaxyElement.style.opacity = "1";

    // Add wheel listener
    window.addEventListener("wheel", handleWheel, { passive: false });

    // Cleanup
    return () => {
      window.removeEventListener("wheel", handleWheel);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [galaxyId, textId, fadeDistance]);

  return null;
};

export default ScrollFadeHandler;
