import React, {
  useEffect,
  useState,
  useImperativeHandle,
  forwardRef,
  useCallback,
} from "react";

interface DynamicHomepageHookProps {
  className?: string;
  phrases?: string[];
  style?: string;
}

interface DynamicHomepageHookRef {
  randomize: () => void;
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

const DynamicHomepageHook = forwardRef<
  DynamicHomepageHookRef,
  DynamicHomepageHookProps
>(({ className = "", phrases = DEFAULT_PHRASES, style = "" }, ref) => {
  const [selectedPhrase, setSelectedPhrase] = useState<string>("");

  const randomizePhrase = useCallback(() => {
    const randomIndex = Math.floor(Math.random() * phrases.length);
    setSelectedPhrase(phrases[randomIndex]);
  }, [phrases]);

  useEffect(() => {
    // Client-side random selection to avoid hydration mismatch
    randomizePhrase();
  }, [randomizePhrase]);

  // Expose randomize method to parent components
  useImperativeHandle(
    ref,
    () => ({
      randomize: randomizePhrase,
    }),
    [randomizePhrase],
  );

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
});

DynamicHomepageHook.displayName = "DynamicHomepageHook";

export default DynamicHomepageHook;
export type { DynamicHomepageHookRef };
