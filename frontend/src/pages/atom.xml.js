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
      .slice(0, 20); // Limit to 20 most recent posts for performance

    const lastUpdated =
      publishedPosts.length > 0
        ? new Date(publishedPosts[0].data.date).toISOString()
        : new Date().toISOString();

    const atomFeed = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>${escapeXml(config.site.title)}</title>
  <subtitle>${escapeXml(config.metadata.meta_description)}</subtitle>
  <link href="${config.site.base_url}/atom.xml" rel="self" type="application/atom+xml"/>
  <link href="${config.site.base_url}/" rel="alternate" type="text/html"/>
  <updated>${lastUpdated}</updated>
  <id>${config.site.base_url}/</id>
  <author>
    <name>${escapeXml(config.metadata.meta_author)}</name>
    <email>${config.params.contact_form_action || "noreply@colemorton.com"}</email>
    <uri>${config.site.base_url}/</uri>
  </author>
  <generator uri="https://astro.build/" version="5.7.8">Astro</generator>
  <rights>Copyright © ${new Date().getFullYear()} ${escapeXml(config.metadata.meta_author)}</rights>

  ${publishedPosts
    .map((post) => {
      const postUrl = `${config.site.base_url}/blog/${post.id}/`;
      const publishedDate = new Date(post.data.date).toISOString();

      return `<entry>
    <title type="html">${escapeXml(post.data.title)}</title>
    <link href="${postUrl}" rel="alternate" type="text/html"/>
    <id>${postUrl}</id>
    <published>${publishedDate}</published>
    <updated>${publishedDate}</updated>
    <author>
      <name>${escapeXml(post.data.author || config.metadata.meta_author)}</name>
    </author>
    <summary type="html">${escapeXml(post.data.description || post.data.summary || "")}</summary>
    <content type="html">${escapeXml(post.body || "")}</content>
    ${post.data.categories ? post.data.categories.map((cat) => `<category term="${escapeXml(cat)}" />`).join("\n    ") : ""}
    ${post.data.tags ? post.data.tags.map((tag) => `<category term="${escapeXml(tag)}" scheme="tag" />`).join("\n    ") : ""}
  </entry>`;
    })
    .join("\n\n  ")}
</feed>`;

    return new Response(atomFeed, {
      headers: {
        "Content-Type": "application/atom+xml; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
      },
    });
  } catch (error) {
    throw new Error(`Failed to generate Atom feed: ${error.message}`);
  }
}

function escapeXml(text) {
  if (typeof text !== "string") {
    return "";
  }
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}
