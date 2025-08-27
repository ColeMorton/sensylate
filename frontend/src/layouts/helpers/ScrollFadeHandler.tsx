import React, { useEffect, useRef, useState } from "react";
import { type GalaxyAnimationRef } from "./GalaxyAnimation";
import { type DynamicHomepageHookRef } from "./DynamicHomepageHook";

type AnimationState =
  | "initial"
  | "fading"
  | "cards-animating"
  | "cards-complete"
  | "reverse-fading";

interface ScrollFadeHandlerProps {
  textId: string;
  fadeDistance?: number;
  galaxyRef: React.RefObject<GalaxyAnimationRef | null>;
  galaxyReady: boolean;
  textRef: React.RefObject<DynamicHomepageHookRef | null>;
  onCardsAnimationStart?: () => void;
  onCardsComplete?: () => void;
  onCardsHiding?: () => void;
}

const ScrollFadeHandler: React.FC<ScrollFadeHandlerProps> = ({
  textId,
  fadeDistance = 800,
  galaxyRef,
  galaxyReady,
  textRef,
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
  const galaxyAnimationStartRef = useRef<number>(0);
  const galaxyStartOpacityRef = useRef<number>(0.5);
  const animationStartupTimeRef = useRef<number>(0);

  // Animation cancellation flags to prevent race conditions
  const animationCancelledRef = useRef<boolean>(false);
  const animationIdRef = useRef<number>(0);

  // Animation locking to prevent overlapping animations during state transitions
  const animationLockRef = useRef<boolean>(false);

  // Create refs to hold fresh values for animation and event handlers
  const galaxyReadyRef = useRef(galaxyReady);
  galaxyReadyRef.current = galaxyReady;

  const animationStateRef = useRef(animationState);
  animationStateRef.current = animationState;

  // Create refs for callbacks to avoid dependency issues
  const onCardsAnimationStartRef = useRef(onCardsAnimationStart);
  onCardsAnimationStartRef.current = onCardsAnimationStart;

  const onCardsCompleteRef = useRef(onCardsComplete);
  onCardsCompleteRef.current = onCardsComplete;

  const onCardsHidingRef = useRef(onCardsHiding);
  onCardsHidingRef.current = onCardsHiding;

  // Track animation completion states
  const forwardAnimationCompletedRef = useRef(false);
  const reverseAnimationCompletedRef = useRef(false);

  const animateGalaxyRef =
    useRef<
      (
        targetOpacity: number,
        duration?: number,
        onComplete?: () => void,
      ) => void
    >();

  // Initialize animation function once
  if (!animateGalaxyRef.current) {
    animateGalaxyRef.current = (
      targetOpacity: number,
      duration: number = 800,
      onComplete?: () => void,
    ) => {
      const currentGalaxyReady = galaxyReadyRef.current;

      if (!currentGalaxyReady || !galaxyRef.current) {
        return;
      }

      // Check if animations are locked (during state transitions)
      if (animationLockRef.current) {
        return;
      }

      // Set animation lock to prevent overlapping animations
      animationLockRef.current = true;

      // Cancel any existing galaxy animation
      if (galaxyAnimationRef.current) {
        clearInterval(galaxyAnimationRef.current);
      }

      // Reset cancellation flag and create new animation ID
      animationCancelledRef.current = false;
      animationIdRef.current += 1;
      const currentAnimationId = animationIdRef.current;

      galaxyAnimationStartRef.current = performance.now();
      animationStartupTimeRef.current = performance.now();

      // Get current opacity from the galaxy component
      try {
        galaxyStartOpacityRef.current = galaxyRef.current.getOpacity();
      } catch {
        galaxyStartOpacityRef.current = 0.5;
      }

      const startTime = performance.now();

      const intervalAnimation = () => {
        const currentTime = performance.now();
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function for smooth animation
        const easeProgress = progress * (2 - progress);

        const currentOpacity =
          galaxyStartOpacityRef.current +
          (targetOpacity - galaxyStartOpacityRef.current) * easeProgress;

        // Validate ref before each frame
        if (!galaxyRef.current) {
          if (galaxyAnimationRef.current) {
            clearInterval(galaxyAnimationRef.current);
            galaxyAnimationRef.current = undefined;
          }
          animationLockRef.current = false;
          return;
        }

        // Use the galaxy component's setOpacity method with error handling
        try {
          galaxyRef.current.setOpacity(currentOpacity);
        } catch {
          if (galaxyAnimationRef.current) {
            clearInterval(galaxyAnimationRef.current);
            galaxyAnimationRef.current = undefined;
          }
          animationLockRef.current = false;
          return;
        }

        if (progress >= 1) {
          if (galaxyAnimationRef.current) {
            clearInterval(galaxyAnimationRef.current);
            galaxyAnimationRef.current = undefined;
          }

          // Release animation lock
          animationLockRef.current = false;

          // Only execute completion callback if animation wasn't cancelled and is still current
          if (
            !animationCancelledRef.current &&
            currentAnimationId === animationIdRef.current &&
            onComplete
          ) {
            onComplete();
          }
        }
      };

      // Execute first frame synchronously
      intervalAnimation();

      // Check if animation completed in first frame
      const elapsed = performance.now() - galaxyAnimationStartRef.current;
      const currentProgress = Math.min(elapsed / duration, 1);

      // Continue with setInterval if not complete
      if (currentProgress < 1) {
        const intervalId = setInterval(intervalAnimation, 16);
        galaxyAnimationRef.current = intervalId as unknown as number;
      }
    };
  }

  useEffect(() => {
    const textElement = document.getElementById(textId);

    if (!textElement) {
      throw new Error(
        `ScrollFadeHandler: Element with ID "${textId}" not found`,
      );
    }

    const handleWheel = (event: WheelEvent) => {
      const isScrollingDown = event.deltaY > 0;

      // Prevent default scrolling behavior
      event.preventDefault();

      // Block scroll handling until galaxy is ready
      if (!galaxyReady) {
        return;
      }

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
        const textFadeThreshold = fadeDistance / 2;
        const cardsAnimationThreshold = fadeDistance;

        // Calculate opacities
        const newTextOpacity =
          scrollProgressRef.current <= textFadeThreshold
            ? Math.max(0, 1 - (scrollProgressRef.current * 2) / fadeDistance)
            : 0;

        // Galaxy opacity calculation
        let galaxyOpacity;
        if (scrollProgressRef.current <= textFadeThreshold) {
          galaxyOpacity = Math.max(
            0.5,
            1 - scrollProgressRef.current / (fadeDistance / 2),
          );
        } else {
          if (forwardAnimationCompletedRef.current) {
            galaxyOpacity = 0.0;
          } else if (reverseAnimationCompletedRef.current) {
            galaxyOpacity = 0.5;
          } else {
            galaxyOpacity = 0.5;
          }
        }

        textElement.style.opacity = newTextOpacity.toString();

        // Galaxy opacity: only set if not currently animating
        const animationActive = !!galaxyAnimationRef.current;
        if (
          !animationActive &&
          animationStateRef.current !== "cards-animating"
        ) {
          try {
            if (galaxyRef.current && galaxyReady) {
              galaxyRef.current.setOpacity(galaxyOpacity);
            }
          } catch {
            // Handle error silently
          }
        }

        // Handle state transitions based on scroll progress and direction
        const previousState = animationStateRef.current;
        let newState = animationStateRef.current;

        if (scrollProgressRef.current === 0) {
          newState = "initial";

          // Reset animation completion flags
          if (
            forwardAnimationCompletedRef.current ||
            reverseAnimationCompletedRef.current
          ) {
            forwardAnimationCompletedRef.current = false;
            reverseAnimationCompletedRef.current = false;
          }

          // Cancel animation if scrolled back to initial
          if (galaxyAnimationRef.current) {
            animationCancelledRef.current = true;
            animationLockRef.current = false;
            clearInterval(galaxyAnimationRef.current);
            galaxyAnimationRef.current = undefined;

            // Reset card state when returning to initial
            onCardsHidingRef.current?.();
          }
        } else if (
          scrollProgressRef.current > 0 &&
          scrollProgressRef.current < textFadeThreshold
        ) {
          newState = isScrollingDown ? "fading" : "reverse-fading";

          // Reset animation completion flags
          if (
            forwardAnimationCompletedRef.current ||
            reverseAnimationCompletedRef.current
          ) {
            forwardAnimationCompletedRef.current = false;
            reverseAnimationCompletedRef.current = false;
          }

          // Cancel animation if scrolled back to text phase
          if (
            previousState === "cards-animating" &&
            galaxyAnimationRef.current
          ) {
            animationCancelledRef.current = true;
            animationLockRef.current = false;
            clearInterval(galaxyAnimationRef.current);
            galaxyAnimationRef.current = undefined;

            // Reset card state when animation is cancelled
            onCardsHidingRef.current?.();
          }
        } else if (
          scrollProgressRef.current >= textFadeThreshold &&
          scrollProgressRef.current < cardsAnimationThreshold
        ) {
          newState = "cards-animating";
        } else if (scrollProgressRef.current >= cardsAnimationThreshold) {
          const timeSinceAnimationStart =
            performance.now() - animationStartupTimeRef.current;
          const inStartupPeriod = timeSinceAnimationStart < 800;
          const animationActive = !!galaxyAnimationRef.current;

          if (!animationActive && !inStartupPeriod) {
            newState = "cards-complete";
          } else {
            newState = previousState;
          }
        }

        // Trigger callbacks on state changes
        if (newState !== previousState) {
          setAnimationState(newState);

          if (newState === "cards-animating" && previousState === "fading") {
            if (galaxyReady && galaxyRef.current) {
              // Forward: cards slide UP, galaxy fades 0.5 → 0.0
              animateGalaxyRef.current?.(0.0, 800, () => {
                // Validate animation is still relevant to current state
                const currentState = animationStateRef.current;
                const currentScrollProgress = scrollProgressRef.current;

                // Only proceed if we're still in forward animation context
                if (
                  currentState !== "cards-animating" &&
                  currentState !== "cards-complete"
                ) {
                  return;
                }

                // Additional check: ensure we're still in the cards animation range
                if (currentScrollProgress < textFadeThreshold) {
                  return;
                }

                // Mark forward animation as completed
                forwardAnimationCompletedRef.current = true;
                reverseAnimationCompletedRef.current = false;

                // Randomize text when galaxy completely disappears
                textRef.current?.randomize();

                // Check if we should transition to cards-complete
                if (currentScrollProgress >= cardsAnimationThreshold) {
                  setAnimationState("cards-complete");
                  onCardsCompleteRef.current?.();
                }
              });
              onCardsAnimationStartRef.current?.();
            }
          } else if (
            newState === "cards-animating" &&
            previousState === "cards-complete"
          ) {
            if (galaxyReady && galaxyRef.current) {
              // Reverse: cards slide DOWN, galaxy fades 0.0 → 0.5
              animateGalaxyRef.current?.(0.5, 800, () => {
                // Validate animation is still relevant to current state
                const currentState = animationStateRef.current;
                const currentScrollProgress = scrollProgressRef.current;

                // Only proceed if we're still in reverse animation context
                if (
                  currentState !== "cards-animating" &&
                  currentState !== "reverse-fading"
                ) {
                  return;
                }

                // Additional check: ensure we're in reverse scroll context
                if (currentScrollProgress >= cardsAnimationThreshold) {
                  return;
                }

                // Mark reverse animation as completed
                reverseAnimationCompletedRef.current = true;
                forwardAnimationCompletedRef.current = false;

                // Transition to reverse-fading
                setAnimationState("reverse-fading");
              });
              onCardsHidingRef.current?.();
            }
          }
        }

        isThrottledRef.current = false;
      });
    };

    // Set initial opacities only once
    if (!initializedRef.current) {
      textElement.style.opacity = "1";

      // Set galaxy initial opacity with retry
      const setInitialGalaxyOpacity = (retryCount = 0) => {
        try {
          if (galaxyRef.current) {
            galaxyRef.current.setOpacity(1);
            initializedRef.current = true;
          } else if (retryCount < 5) {
            setTimeout(() => setInitialGalaxyOpacity(retryCount + 1), 100);
          }
        } catch {
          // Handle error silently
        }
      };

      setInitialGalaxyOpacity();
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
        animationCancelledRef.current = true;
        animationLockRef.current = false;
        clearInterval(galaxyAnimationRef.current);
        galaxyAnimationRef.current = undefined;
      }
    };
  }, [galaxyRef, galaxyReady, textRef, textId, fadeDistance]);

  return null;
};

export default ScrollFadeHandler;
