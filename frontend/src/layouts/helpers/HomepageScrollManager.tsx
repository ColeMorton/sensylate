import React, { useState } from "react";
import ScrollFadeHandler from "./ScrollFadeHandler";
import PinnedCardsHandler from "./PinnedCardsHandler";

type CardDirection = "hidden" | "showing" | "visible" | "hiding";

interface HomepageScrollManagerProps {
  galaxyId: string;
  textId: string;
  fadeDistance?: number;
}

const HomepageScrollManager: React.FC<HomepageScrollManagerProps> = ({
  galaxyId,
  textId,
  fadeDistance = 800,
}) => {
  const [cardDirection, setCardDirection] = useState<CardDirection>("hidden");

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

  return (
    <>
      <ScrollFadeHandler
        galaxyId={galaxyId}
        textId={textId}
        fadeDistance={fadeDistance}
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
