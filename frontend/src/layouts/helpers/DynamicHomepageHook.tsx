import React, { useEffect, useState } from "react";

interface DynamicHomepageHookProps {
  className?: string;
  phrases?: string[];
  style?: string;
}

const DEFAULT_PHRASES = [
  "I built an AI team that turns market chaos into human clarity.",
  "What if complex financial data could think its way to simplicity?",
  "My AI agents collaborate so you don't have to decode markets alone.",
  "89% faster insights when artificial intelligence works as a team.",
  "I don't just analyze markets - I've automated the art of making sense.",
  "Complex market signals → AI collaboration → insights you actually understand.",
  "While others dump data, my AI refinery delivers clarity.",
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
