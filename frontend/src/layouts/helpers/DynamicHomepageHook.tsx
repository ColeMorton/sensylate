import React, { useEffect, useState } from "react";

interface DynamicHomepageHookProps {
  className?: string;
  phrases?: string[];
  style?: string;
}

const DEFAULT_PHRASES = [
  "Turn market chaos into human clarity.",
  "What if complex financial data could think its way to simplicity?",
  "When AI agents collaborate - you don't have to decode markets alone.",
  "Don't just analyze markets - automate the art of making sense.",
  "Complex market signals → AI collaboration → insights you actually understand.",
  "While others dump data, my AI refinery delivers clarity.",
  "What if your market analysis had a team of AI specialists behind it?",
  "From raw market data to clear insights in four automated steps.",
  "18+ data sources, one systematic process, insights you can trust.",
  "My AI doesn't guess - it validates everything across multiple sources.",
  "Beyond gut feelings: systematic analysis that scales with the markets.",
];

const DynamicHomepageHook: React.FC<DynamicHomepageHookProps> = ({
  className = "",
  phrases = DEFAULT_PHRASES,
  style = "",
}) => {
  const [selectedPhrase, setSelectedPhrase] = useState<string>("");

  useEffect(() => {
    // Client-side random selection to avoid hydration mismatch
    const randomIndex = Math.floor(Math.random() * phrases.length);
    setSelectedPhrase(phrases[randomIndex]);
  }, [phrases]);

  return (
    <h2
      className={className}
      style={
        style
          ? { marginTop: style.replace("margin-top: ", "").replace(";", "") }
          : undefined
      }
    >
      {selectedPhrase}
    </h2>
  );
};

export default DynamicHomepageHook;
