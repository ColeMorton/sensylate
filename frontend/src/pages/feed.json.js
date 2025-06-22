import { getSinglePage } from "@/lib/contentParser.astro";
import config from "@/config/config.json";

export async function GET(_context) {
  try {
    // Get all blog posts
    const posts = await getSinglePage("blog");

    // Filter out draft posts and sort by date (newest first)
    const publishedPosts = posts
      .filter((post) => !post.data.draft)
      .sort((a, b) => new Date(b.data.date) - new Date(a.data.date))
      .slice(0, 50); // Limit to 50 most recent posts

    const jsonFeed = {
      version: "https://jsonfeed.org/version/1.1",
      title: config.site.title,
      description: config.metadata.meta_description,
      home_page_url: config.site.base_url,
      feed_url: `${config.site.base_url}/feed.json`,
      language: "en-US",
      favicon: `${config.site.base_url}/images/favicon.png`,
      icon: `${config.site.base_url}/images/android-chrome-512x512.png`,
      authors: [
        {
          name: config.metadata.meta_author,
          url: config.site.base_url,
          avatar: `${config.site.base_url}/images/android-chrome-192x192.png`,
        },
      ],
      items: publishedPosts.map((post) => ({
        id: `${config.site.base_url}/blog/${post.id}/`,
        url: `${config.site.base_url}/blog/${post.id}/`,
        title: post.data.title,
        content_html: post.body || "",
        content_text: stripHtml(post.body || ""),
        summary: post.data.description || post.data.summary || "",
        image: post.data.image
          ? `${config.site.base_url}${post.data.image}`
          : null,
        date_published: new Date(post.data.date).toISOString(),
        date_modified: new Date(post.data.date).toISOString(),
        authors: [
          {
            name: post.data.author || config.metadata.meta_author,
            url: config.site.base_url,
          },
        ],
        tags: [...(post.data.categories || []), ...(post.data.tags || [])],
        language: "en-US",
        _trading_strategy: {
          symbols: extractSymbols(post.data.title, post.body),
          rating: extractRating(post.data.title, post.body),
          analysis_type: post.data.categories?.includes("fundamental-analysis")
            ? "fundamental"
            : post.data.categories?.includes("technical-analysis")
              ? "technical"
              : "general",
        },
      })),
    };

    return new Response(JSON.stringify(jsonFeed, null, 2), {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "public, max-age=3600, stale-while-revalidate=86400",
      },
    });
  } catch (error) {
    throw new Error(`Failed to generate JSON feed: ${error.message}`);
  }
}

function stripHtml(html) {
  if (typeof html !== "string") {
    return "";
  }
  return html
    .replace(/<[^>]*>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractSymbols(title, content) {
  const text = `${title} ${content || ""}`;
  const symbols = text.match(/\b[A-Z]{2,5}\b/g) || [];
  // Filter for common stock symbols and remove common words
  const commonWords = [
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
    "BUT",
    "HOW",
    "WHO",
    "DID",
    "YES",
    "HIS",
    "HAS",
    "HAD",
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
    "MAD",
    "BOY",
    "DIG",
    "BIG",
    "BAD",
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
    "LET",
    "PUT",
    "SAY",
    "SIX",
    "DOG",
    "EGG",
    "AGO",
    "SIT",
    "FUN",
    "BAD",
    "YES",
    "YET",
    "OUT",
    "CUT",
    "BUY",
    "LOT",
    "CAR",
    "EAT",
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
    "ETF",
    "SMA",
    "RSI",
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
  ];
  return [
    ...new Set(
      symbols.filter(
        (symbol) =>
          !commonWords.includes(symbol) &&
          symbol.length >= 2 &&
          symbol.length <= 5,
      ),
    ),
  ];
}

function extractRating(title, content) {
  const text = `${title} ${content || ""}`.toLowerCase();
  if (text.includes("buy") || text.includes("strong buy")) {
    return "buy";
  }
  if (text.includes("sell") || text.includes("strong sell")) {
    return "sell";
  }
  if (text.includes("hold")) {
    return "hold";
  }
  return null;
}
