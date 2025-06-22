/**
 * Content Analysis Utilities for SEO Enhancement
 * Provides reading time estimation, word count, and content quality metrics
 */

export interface ContentMetrics {
  wordCount: number;
  readingTimeMinutes: number;
  readingTimeText: string;
  characterCount: number;
  paragraphCount: number;
  estimatedSeoScore: number;
}

export interface ReadingTimeOptions {
  wordsPerMinute?: number;
  includeCodeBlocks?: boolean;
  includeImages?: boolean;
  imageReadingTime?: number; // seconds per image
}

/**
 * Calculates comprehensive content metrics for blog posts
 */
export function analyzeContent(
  content: string,
  options: ReadingTimeOptions = {},
): ContentMetrics {
  const {
    wordsPerMinute = 200, // Average adult reading speed
    includeCodeBlocks = true,
    includeImages = true,
    imageReadingTime = 12, // 12 seconds per image (industry standard)
  } = options;

  // Clean content for analysis
  const cleanContent = stripMarkdown(content);

  // Word count calculation
  const wordCount = countWords(cleanContent);

  // Character count (excluding HTML/Markdown)
  const characterCount = cleanContent.length;

  // Paragraph count
  const paragraphCount = countParagraphs(content);

  // Base reading time calculation
  let readingTimeMinutes = wordCount / wordsPerMinute;

  // Add time for code blocks
  if (includeCodeBlocks) {
    const codeBlockCount = countCodeBlocks(content);
    readingTimeMinutes += codeBlockCount * 0.5; // 30 seconds per code block
  }

  // Add time for images
  if (includeImages) {
    const imageCount = countImages(content);
    readingTimeMinutes += (imageCount * imageReadingTime) / 60;
  }

  // Ensure minimum reading time
  readingTimeMinutes = Math.max(readingTimeMinutes, 0.5);

  // Generate reading time text
  const readingTimeText = formatReadingTime(readingTimeMinutes);

  // Calculate estimated SEO score
  const estimatedSeoScore = calculateSeoScore({
    wordCount,
    characterCount,
    paragraphCount,
    readingTimeMinutes,
  });

  return {
    wordCount: Math.round(wordCount),
    readingTimeMinutes: Math.round(readingTimeMinutes),
    readingTimeText,
    characterCount,
    paragraphCount,
    estimatedSeoScore,
  };
}

/**
 * Quick reading time calculation for simple use cases
 */
export function calculateReadingTime(
  content: string,
  wordsPerMinute: number = 200,
): { minutes: number; text: string } {
  const metrics = analyzeContent(content, { wordsPerMinute });
  return {
    minutes: metrics.readingTimeMinutes,
    text: metrics.readingTimeText,
  };
}

/**
 * Removes Markdown formatting and HTML tags for clean text analysis
 */
function stripMarkdown(content: string): string {
  return (
    content
      // Remove HTML tags
      .replace(/<[^>]*>/g, "")
      // Remove Markdown links [text](url)
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      // Remove Markdown images ![alt](url)
      .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
      // Remove Markdown headers
      .replace(/^#{1,6}\s+/gm, "")
      // Remove Markdown emphasis and strong
      .replace(/\*\*([^*]+)\*\*/g, "$1")
      .replace(/\*([^*]+)\*/g, "$1")
      .replace(/__([^_]+)__/g, "$1")
      .replace(/_([^_]+)_/g, "$1")
      // Remove Markdown code blocks
      .replace(/```[\s\S]*?```/g, "")
      // Remove inline code
      .replace(/`([^`]+)`/g, "$1")
      // Remove blockquotes
      .replace(/^>\s+/gm, "")
      // Remove horizontal rules
      .replace(/^[-*_]{3,}$/gm, "")
      // Remove extra whitespace
      .replace(/\s+/g, " ")
      .trim()
  );
}

/**
 * Counts words in clean text
 */
function countWords(text: string): number {
  if (!text || text.trim().length === 0) {
    return 0;
  }

  return text
    .trim()
    .split(/\s+/)
    .filter((word) => word.length > 0).length;
}

/**
 * Counts paragraphs in content
 */
function countParagraphs(content: string): number {
  return content
    .split(/\n\s*\n/)
    .filter((paragraph) => paragraph.trim().length > 0).length;
}

/**
 * Counts code blocks in Markdown content
 */
function countCodeBlocks(content: string): number {
  const codeBlockRegex = /```[\s\S]*?```/g;
  return (content.match(codeBlockRegex) || []).length;
}

/**
 * Counts images in Markdown content
 */
function countImages(content: string): number {
  const imageRegex = /!\[([^\]]*)\]\([^)]+\)/g;
  return (content.match(imageRegex) || []).length;
}

/**
 * Formats reading time into human-readable text
 */
function formatReadingTime(minutes: number): string {
  const roundedMinutes = Math.round(minutes);

  if (roundedMinutes < 1) {
    return "Less than 1 min read";
  } else if (roundedMinutes === 1) {
    return "1 min read";
  } else if (roundedMinutes < 60) {
    return `${roundedMinutes} min read`;
  } else {
    const hours = Math.floor(roundedMinutes / 60);
    const remainingMinutes = roundedMinutes % 60;

    if (remainingMinutes === 0) {
      return hours === 1 ? "1 hour read" : `${hours} hours read`;
    } else {
      return `${hours}h ${remainingMinutes}m read`;
    }
  }
}

/**
 * Calculates estimated SEO score based on content metrics
 */
function calculateSeoScore(metrics: {
  wordCount: number;
  characterCount: number;
  paragraphCount: number;
  readingTimeMinutes: number;
}): number {
  let score = 0;

  // Word count scoring (optimal: 1500-2500 words for trading content)
  if (metrics.wordCount >= 1500 && metrics.wordCount <= 2500) {
    score += 30;
  } else if (metrics.wordCount >= 1000 && metrics.wordCount < 1500) {
    score += 25;
  } else if (metrics.wordCount >= 2500 && metrics.wordCount <= 3500) {
    score += 25;
  } else if (metrics.wordCount >= 500 && metrics.wordCount < 1000) {
    score += 15;
  } else {
    score += 5;
  }

  // Reading time scoring (optimal: 5-15 minutes for financial analysis)
  if (metrics.readingTimeMinutes >= 5 && metrics.readingTimeMinutes <= 15) {
    score += 25;
  } else if (
    metrics.readingTimeMinutes >= 3 &&
    metrics.readingTimeMinutes < 5
  ) {
    score += 20;
  } else if (
    metrics.readingTimeMinutes > 15 &&
    metrics.readingTimeMinutes <= 25
  ) {
    score += 20;
  } else {
    score += 10;
  }

  // Paragraph structure scoring (optimal: 8-20 paragraphs)
  if (metrics.paragraphCount >= 8 && metrics.paragraphCount <= 20) {
    score += 20;
  } else if (metrics.paragraphCount >= 5 && metrics.paragraphCount < 8) {
    score += 15;
  } else if (metrics.paragraphCount > 20 && metrics.paragraphCount <= 30) {
    score += 15;
  } else {
    score += 5;
  }

  // Content depth scoring (character count as proxy)
  if (metrics.characterCount >= 8000 && metrics.characterCount <= 15000) {
    score += 15;
  } else if (metrics.characterCount >= 5000 && metrics.characterCount < 8000) {
    score += 12;
  } else if (
    metrics.characterCount > 15000 &&
    metrics.characterCount <= 25000
  ) {
    score += 12;
  } else {
    score += 5;
  }

  // Readability bonus (balanced reading time vs content length)
  const wordsPerMinute =
    metrics.wordCount / Math.max(metrics.readingTimeMinutes, 1);
  if (wordsPerMinute >= 180 && wordsPerMinute <= 220) {
    score += 10; // Good balance
  } else if (wordsPerMinute >= 150 && wordsPerMinute < 180) {
    score += 7; // Slightly slower, but detailed
  } else if (wordsPerMinute > 220 && wordsPerMinute <= 250) {
    score += 7; // Slightly faster, but concise
  } else {
    score += 3;
  }

  return Math.min(score, 100);
}

/**
 * Extracts key trading symbols from content for enhanced meta tags
 */
export function extractTradingSymbols(
  content: string,
  title: string = "",
): string[] {
  const text = `${title} ${content}`;

  // Look for stock symbols (2-5 uppercase letters, often in parentheses or standalone)
  const symbolPattern = /\b([A-Z]{2,5})\b/g;
  const potentialSymbols = Array.from(
    text.matchAll(symbolPattern),
    (m) => m[1],
  );

  // Common words to exclude from symbol detection
  const excludeWords = new Set([
    "THE",
    "AND",
    "FOR",
    "ARE",
    "BUT",
    "NOT",
    "YOU",
    "ALL",
    "CAN",
    "HER",
    "WAS",
    "ONE",
    "OUR",
    "HAD",
    "HOW",
    "WHO",
    "DID",
    "YES",
    "HIS",
    "HAS",
    "LET",
    "PUT",
    "TOO",
    "OLD",
    "ANY",
    "MAY",
    "SAY",
    "SHE",
    "USE",
    "ITS",
    "NOW",
    "WAY",
    "DAY",
    "MAN",
    "NEW",
    "SEE",
    "TWO",
    "GOT",
    "GET",
    "OWN",
    "SAW",
    "SUN",
    "SET",
    "RUN",
    "EAT",
    "FAR",
    "SEA",
    "EYE",
    "RED",
    "TOP",
    "ARM",
    "OFF",
    "TRY",
    "END",
    "WHY",
    "SIX",
    "DOG",
    "EGG",
    "AGO",
    "SIT",
    "FUN",
    "BAD",
    "YET",
    "OUT",
    "CUT",
    "BUY",
    "LOT",
    "CAR",
    "JOB",
    "WIN",
    "PAN",
    "BAG",
    "TEA",
    "CUP",
    "BED",
    "BOX",
    "WAR",
    "FAD",
    "BAT",
    "GOD",
    "OIL",
    "PIE",
    "AGE",
    "POP",
    "ART",
    "KEY",
    "TAX",
    "LAW",
    "GAS",
    "LED",
    "BET",
    "DUE",
    "ETC",
    "CEO",
    "CFO",
    "IPO",
    "SEC",
    "FDA",
    "GDP",
    "API",
    "URL",
    "PDF",
    "XML",
    "CSS",
    "HTML",
    "AWS",
    "USD",
    "EUR",
    "GBP",
    "LLC",
    "INC",
    "LTD",
    "COR",
    "ETF",
    "SMA",
    "RSI",
    "ROI",
    "TTM",
    "YOY",
    "QOQ",
    "LTM",
  ]);

  // Filter and deduplicate symbols
  const symbols = [...new Set(potentialSymbols)]
    .filter((symbol) => !excludeWords.has(symbol))
    .filter((symbol) => symbol.length >= 2 && symbol.length <= 5)
    .slice(0, 5); // Limit to top 5 symbols

  return symbols;
}

/**
 * Generates enhanced keywords from content analysis
 */
export function generateContentKeywords(
  content: string,
  title: string = "",
  categories: string[] = [],
  tags: string[] = [],
): string[] {
  const symbols = extractTradingSymbols(content, title);
  const baseKeywords = [
    "trading strategy",
    "fundamental analysis",
    "investment research",
    "market analysis",
    "financial analysis",
  ];

  const categoryKeywords = categories.map((cat) =>
    cat.toLowerCase().replace("-", " "),
  );
  const tagKeywords = tags.map((tag) => tag.toLowerCase().replace("-", " "));

  // Combine and deduplicate
  return [
    ...new Set([
      ...baseKeywords,
      ...categoryKeywords,
      ...tagKeywords,
      ...symbols.map((s) => s.toLowerCase()),
      "Cole Morton",
      "quantitative analysis",
      "systematic trading",
    ]),
  ].slice(0, 15); // Limit to 15 keywords for optimal SEO
}
