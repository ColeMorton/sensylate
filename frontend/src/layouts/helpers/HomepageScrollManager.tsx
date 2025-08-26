import React, { useState, useRef, useEffect, useCallback } from "react";
import ScrollFadeHandler from "./ScrollFadeHandler";
import PinnedCardsHandler from "./PinnedCardsHandler";
import GalaxyAnimation, { type GalaxyAnimationRef } from "./GalaxyAnimation";

type CardDirection = "hidden" | "showing" | "visible" | "hiding";

interface HomepageScrollManagerProps {
  textId: string;
  fadeDistance?: number;
}

const HomepageScrollManager: React.FC<HomepageScrollManagerProps> = ({
  textId,
  fadeDistance = 800,
}) => {
  const [cardDirection, setCardDirection] = useState<CardDirection>("hidden");
  const [galaxyReady, setGalaxyReady] = useState(false);
  const galaxyRef = useRef<GalaxyAnimationRef>(null);

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
      {/* Render GalaxyAnimation directly with fixed positioning to target container */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          pointerEvents: "none",
          zIndex: 0,
        }}
      >
        <GalaxyAnimation
          ref={galaxyRef}
          className="absolute inset-0"
          onReady={handleGalaxyReady}
        />
      </div>

      <ScrollFadeHandler
        textId={textId}
        fadeDistance={fadeDistance}
        galaxyRef={galaxyRef}
        galaxyReady={galaxyReady}
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
