import rss from "@astrojs/rss";
import { getSinglePage } from "@/lib/contentParser.astro";
import config from "@/config/config.json";

export async function GET(_context) {
  try {
    // Get all blog posts
    const posts = await getSinglePage("blog");

    // Filter out draft posts and sort by date (newest first)
    const publishedPosts = posts
      .filter((post) => !post.data.draft)
      .sort((a, b) => new Date(b.data.date) - new Date(a.data.date));

    return rss({
      title: config.site.title,
      description: config.metadata.meta_description,
      site: config.site.base_url,
      items: publishedPosts.map((post) => ({
        title: post.data.title,
        description: post.data.description || post.data.summary || "",
        pubDate: new Date(post.data.date),
        link: `/blog/${post.id}/`,
        categories: post.data.categories || [],
        author: post.data.author || config.metadata.meta_author,
        content: post.body,
        customData: `
          <guid isPermaLink="false">${config.site.base_url}/blog/${post.id}/</guid>
          ${post.data.image ? `<enclosure url="${config.site.base_url}${post.data.image}" type="image/jpeg" />` : ""}
          ${post.data.tags ? post.data.tags.map((tag) => `<category>${tag}</category>`).join("") : ""}
        `.trim(),
      })),
      customData: `
        <language>en-us</language>
        <managingEditor>${config.params.contact_form_action || "noreply@colemorton.com"} (Cole Morton)</managingEditor>
        <webMaster>${config.params.contact_form_action || "noreply@colemorton.com"} (Cole Morton)</webMaster>
        <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
        <ttl>60</ttl>
        <image>
          <url>${config.site.base_url}/images/favicon.png</url>
          <title>${config.site.title}</title>
          <link>${config.site.base_url}/</link>
        </image>
      `.trim(),
    });
  } catch (error) {
    throw new Error(`Failed to generate RSS feed: ${error.message}`);
  }
}
