import React, { useCallback, useEffect, useRef, useState } from "react";

type AnimationState =
  | "initial"
  | "fading"
  | "cards-animating"
  | "cards-complete"
  | "reverse-fading";

interface ScrollFadeHandlerProps {
  galaxyId: string;
  textId: string;
  fadeDistance?: number;
  onCardsAnimationStart?: () => void;
  onCardsComplete?: () => void;
  onCardsHiding?: () => void;
}

const ScrollFadeHandler: React.FC<ScrollFadeHandlerProps> = ({
  galaxyId,
  textId,
  fadeDistance = 800,
  onCardsAnimationStart,
  onCardsComplete,
  onCardsHiding,
}) => {
  const animationFrameRef = useRef<number>();
  const isThrottledRef = useRef(false);
  const scrollProgressRef = useRef(0);
  const [animationState, setAnimationState] =
    useState<AnimationState>("initial");
  const initializedRef = useRef(false);

  // Galaxy animation state
  const galaxyAnimationRef = useRef<number>();
  const [galaxyAnimating, setGalaxyAnimating] = useState(false);
  const galaxyAnimationStartRef = useRef<number>(0);
  const galaxyStartOpacityRef = useRef<number>(0.5);

  // Galaxy time-based animation function
  const animateGalaxy = useCallback(
    (
      targetOpacity: number,
      duration: number = 800,
      onComplete?: () => void,
    ) => {
      const galaxyElement = document.getElementById(galaxyId);
      if (!galaxyElement) {
        return;
      }

      // Cancel any existing galaxy animation
      if (galaxyAnimationRef.current) {
        cancelAnimationFrame(galaxyAnimationRef.current);
      }

      setGalaxyAnimating(true);
      galaxyAnimationStartRef.current = performance.now();

      // Get actual computed opacity, not just style property
      const computedStyle = window.getComputedStyle(galaxyElement);
      galaxyStartOpacityRef.current = parseFloat(
        computedStyle.opacity || "0.5",
      );

      const animate = (currentTime: number) => {
        const elapsed = currentTime - galaxyAnimationStartRef.current;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function for smooth animation
        const easeProgress = progress * (2 - progress); // ease-out quadratic

        const currentOpacity =
          galaxyStartOpacityRef.current +
          (targetOpacity - galaxyStartOpacityRef.current) * easeProgress;

        galaxyElement.style.opacity = currentOpacity.toString();

        if (progress < 1) {
          galaxyAnimationRef.current = requestAnimationFrame(animate);
        } else {
          setGalaxyAnimating(false);
          onComplete?.(); // Trigger callback when animation completes
        }
      };

      galaxyAnimationRef.current = requestAnimationFrame(animate);
    },
    [galaxyId],
  );

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
      const isScrollingDown = event.deltaY > 0;

      // Prevent default scrolling behavior
      event.preventDefault();

      if (isThrottledRef.current) {
        return;
      }

      isThrottledRef.current = true;
      animationFrameRef.current = requestAnimationFrame(() => {
        // Accumulate scroll progress based on wheel delta
        scrollProgressRef.current += event.deltaY;

        // Clamp scroll progress to full fadeDistance range
        scrollProgressRef.current = Math.max(
          0,
          Math.min(fadeDistance, scrollProgressRef.current),
        );

        // Define stage thresholds
        const textFadeThreshold = fadeDistance / 2; // Text completes at 50%
        const cardsAnimationThreshold = fadeDistance; // Galaxy completes at 100%

        // Calculate opacities
        // Text: Fades 1.0→0.0 in first half (0 to fadeDistance/2)
        const newTextOpacity =
          scrollProgressRef.current <= textFadeThreshold
            ? Math.max(0, 1 - (scrollProgressRef.current * 2) / fadeDistance)
            : 0;

        // Galaxy: Fades 1.0→0.5 during scroll, stays 0.5 during card phase
        const galaxyOpacity =
          scrollProgressRef.current <= textFadeThreshold
            ? Math.max(0.5, 1 - scrollProgressRef.current / (fadeDistance / 2)) // Fades 1.0 → 0.5 in first half
            : 0.5; // Fixed at 0.5 during card phase

        textElement.style.opacity = newTextOpacity.toString();

        // Galaxy opacity: only set if not currently animating with cards AND not in cards-animating state
        if (!galaxyAnimating && animationState !== "cards-animating") {
          galaxyElement.style.opacity = galaxyOpacity.toString();
        }

        // Handle state transitions based on scroll progress and direction
        const previousState = animationState;
        let newState = animationState;

        if (scrollProgressRef.current === 0) {
          newState = "initial";

          // If we were animating and scrolled all the way back, cancel animation
          if (galaxyAnimating) {
            if (galaxyAnimationRef.current) {
              cancelAnimationFrame(galaxyAnimationRef.current);
            }
            setGalaxyAnimating(false);
          }
        } else if (
          scrollProgressRef.current > 0 &&
          scrollProgressRef.current < textFadeThreshold
        ) {
          newState = isScrollingDown ? "fading" : "reverse-fading";

          // If we were in cards-animating and scrolled back to text phase, cancel animation
          if (previousState === "cards-animating" && galaxyAnimating) {
            if (galaxyAnimationRef.current) {
              cancelAnimationFrame(galaxyAnimationRef.current);
            }
            setGalaxyAnimating(false);
          }
        } else if (
          scrollProgressRef.current >= textFadeThreshold &&
          scrollProgressRef.current < cardsAnimationThreshold
        ) {
          newState = isScrollingDown ? "cards-animating" : "cards-animating";
        } else if (scrollProgressRef.current >= cardsAnimationThreshold) {
          newState = "cards-complete";
        }

        // Trigger callbacks on state changes
        if (newState !== previousState) {
          setAnimationState(newState);

          if (newState === "cards-animating" && previousState === "fading") {
            // Forward: cards slide UP, galaxy fades 0.5 → 0.0
            animateGalaxy(0.0);
            onCardsAnimationStart?.();
          } else if (
            newState === "cards-complete" &&
            previousState === "cards-animating"
          ) {
            // Cards animation complete, galaxy should be at 0.0
            onCardsComplete?.();
          } else if (
            newState === "cards-animating" &&
            previousState === "cards-complete"
          ) {
            // Reverse: cards slide DOWN, galaxy fades 0.0 → 0.5
            animateGalaxy(0.5, 800, () => {
              // After reverse animation completes, transition to reverse-fading for scroll control
              setAnimationState("reverse-fading");
            });
            onCardsHiding?.();
          }
        }

        isThrottledRef.current = false;
      });
    };

    // Set initial opacities only once
    if (!initializedRef.current) {
      textElement.style.opacity = "1";
      galaxyElement.style.opacity = "1";
      initializedRef.current = true;
    }

    // Add wheel listener
    window.addEventListener("wheel", handleWheel, { passive: false });

    // Cleanup
    return () => {
      window.removeEventListener("wheel", handleWheel);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (galaxyAnimationRef.current) {
        cancelAnimationFrame(galaxyAnimationRef.current);
      }
    };
  }, [
    galaxyId,
    textId,
    fadeDistance,
    onCardsAnimationStart,
    onCardsComplete,
    onCardsHiding,
    animationState,
    galaxyAnimating,
    animateGalaxy,
  ]);

  return null;
};

export default ScrollFadeHandler;
