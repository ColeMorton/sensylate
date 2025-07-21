import { defineCollection, z } from "astro:content";

// Common schema fields used across collections
const baseSchema = z.object({
  title: z.string(),
  meta_title: z.string().optional(),
  description: z.string().optional(),
  image: z.string().optional(),
  draft: z.boolean().default(false),
});

// Pages collection (charts, elements, privacy-policy, etc.)
const pagesCollection = defineCollection({
  type: "content",
  schema: baseSchema.extend({
    // Additional fields specific to pages can be added here
  }),
});

// Blog collection
const blogCollection = defineCollection({
  type: "content",
  schema: baseSchema.extend({
    date: z.date().optional(),
    authors: z.array(z.string()).default([]),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
  }),
});

// About collection
const aboutCollection = defineCollection({
  type: "content",
  schema: baseSchema,
});

// Calculators collection
const calculatorsCollection = defineCollection({
  type: "content",
  schema: baseSchema,
});

// Contact collection
const contactCollection = defineCollection({
  type: "content",
  schema: baseSchema,
});

// Homepage collection
const homepageCollection = defineCollection({
  type: "content",
  schema: baseSchema,
});

// Sections collection (call-to-action, testimonial, etc.)
const sectionsCollection = defineCollection({
  type: "content",
  schema: baseSchema,
});

export const collections = {
  pages: pagesCollection,
  blog: blogCollection,
  about: aboutCollection,
  calculators: calculatorsCollection,
  contact: contactCollection,
  homepage: homepageCollection,
  sections: sectionsCollection,
};
