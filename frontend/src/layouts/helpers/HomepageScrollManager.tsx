import React, { useState, useRef, useEffect, useCallback } from "react";
import ScrollFadeHandler from "./ScrollFadeHandler";
import PinnedCardsHandler from "./PinnedCardsHandler";
import GalaxyAnimation, { type GalaxyAnimationRef } from "./GalaxyAnimation";
import DynamicHomepageHook, {
  type DynamicHomepageHookRef,
} from "./DynamicHomepageHook";

type CardDirection = "hidden" | "showing" | "visible" | "hiding";

interface HomepageScrollManagerProps {
  textId: string;
  fadeDistance?: number;
  textClassName?: string;
  textStyle?: string;
}

const HomepageScrollManager: React.FC<HomepageScrollManagerProps> = ({
  textId,
  fadeDistance = 800,
  textClassName = "",
  textStyle = "",
}) => {
  const [cardDirection, setCardDirection] = useState<CardDirection>("hidden");
  const [galaxyReady, setGalaxyReady] = useState(false);
  const galaxyRef = useRef<GalaxyAnimationRef>(null);
  const textRef = useRef<DynamicHomepageHookRef>(null);

  const handleCardsAnimationStart = () => {
    setCardDirection("showing");
  };

  const handleCardsComplete = () => {
    setCardDirection("visible");
  };

  const handleCardsHiding = () => {
    setCardDirection("hiding");
  };

  const handleCardsHidden = () => {
    setCardDirection("hidden");
  };

  // Monitor galaxy ref readiness
  useEffect(() => {
    const checkGalaxyReady = () => {
      if (galaxyRef.current) {
        setGalaxyReady(true);
      } else {
        // Retry after a short delay
        setTimeout(checkGalaxyReady, 50);
      }
    };

    checkGalaxyReady();
  }, []);

  // Callback for when galaxy component is initialized - memoized to prevent GalaxyAnimation re-initialization
  const handleGalaxyReady = useCallback(() => {
    setGalaxyReady(true);
  }, []);

  return (
    <>
      {/* Render GalaxyAnimation with absolute positioning within the section */}
      <div className="pointer-events-none absolute inset-0 z-0">
        <GalaxyAnimation
          ref={galaxyRef}
          className="h-full w-full"
          onReady={handleGalaxyReady}
        />
      </div>

      {/* Text content overlay positioned within the section */}
      <div
        id={textId}
        className="absolute inset-0 z-10 flex items-center justify-center"
      >
        <DynamicHomepageHook
          ref={textRef}
          className={textClassName}
          style={textStyle}
        />
      </div>

      <ScrollFadeHandler
        textId={textId}
        fadeDistance={fadeDistance}
        galaxyRef={galaxyRef}
        galaxyReady={galaxyReady}
        textRef={textRef}
        onCardsAnimationStart={handleCardsAnimationStart}
        onCardsComplete={handleCardsComplete}
        onCardsHiding={handleCardsHiding}
      />
      <PinnedCardsHandler
        show={cardDirection === "showing" || cardDirection === "visible"}
        hide={cardDirection === "hiding"}
        onHidden={handleCardsHidden}
      />
    </>
  );
};

export default HomepageScrollManager;
