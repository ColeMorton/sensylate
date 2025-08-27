import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchModal from "../layouts/helpers/SearchModal";

// Mock search data
vi.mock("../../.json/search.json", () => ({
  default: [
    {
      group: "Blog",
      slug: "/test-post-1",
      frontmatter: {
        title: "Test Post 1",
        description: "A comprehensive guide to testing",
        categories: ["technology", "programming"],
        tags: ["astro", "testing", "javascript"],
        image: "/images/test1.jpg",
      },
      content: "This is test content about Astro and testing",
    },
    {
      group: "Blog",
      slug: "/another-test-post",
      frontmatter: {
        title: "Another Test Post",
        description:
          "Comprehensive testing strategies for modern web development",
        categories: ["development", "best-practices"],
        tags: ["testing", "automation"],
        image: "/images/test2.jpg",
      },
      content: "Content about testing strategies and automation",
    },
  ],
}));

// Mock useFeatureFlag hook
vi.mock("@/hooks/useFeatureFlag", () => ({
  useFeatureFlag: vi.fn(() => true), // Search feature enabled by default
}));

describe("SearchModal", () => {
  beforeEach(() => {
    // Reset DOM before each test
    document.body.innerHTML = "";

    // Set up DOM elements that SearchModal expects to find
    // These elements would normally exist in the page layout
    const searchTrigger = document.createElement("button");
    searchTrigger.setAttribute("data-search-trigger", "");
    searchTrigger.textContent = "Search";
    document.body.appendChild(searchTrigger);

    // Clear any existing event listeners
    vi.clearAllMocks();
  });

  it("renders search modal correctly", () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);
    expect(searchInput).toBeInTheDocument();
  });

  it("handles search input changes", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "test" } });

    expect(searchInput).toHaveValue("test");
  });

  it("filters search results based on title", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "Test" } });

    await waitFor(() => {
      const resultLink = screen.getByRole("link", { name: /test post 1/i });
      expect(resultLink).toBeInTheDocument();
    });
  });

  it("filters search results based on description", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, {
      target: { value: "comprehensive testing" },
    });

    await waitFor(() => {
      const results = screen.getByText("Another Test Post");
      expect(results).toBeInTheDocument();
    });
  });

  it("filters search results based on categories", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "technology" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });

  it("filters search results based on tags", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "astro" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });

  it("shows no results when search string does not match", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "nonexistent content" } });

    await waitFor(() => {
      const noResults = screen.getByText(/no results for/i);
      expect(noResults).toBeInTheDocument();
    });
  });

  it("shows empty state when search string is empty", () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "" } });

    // Should not show any results or "no results" message
    expect(screen.queryByText(/no results for/i)).not.toBeInTheDocument();
  });

  it("handles special characters in search input", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    // Test backslash handling (as seen in the component code)
    fireEvent.change(searchInput, { target: { value: "test\\post" } });

    expect(searchInput).toHaveValue("testpost"); // Backslash should be removed
  });

  it("performs case-insensitive search", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search\.\.\./i);

    fireEvent.change(searchInput, { target: { value: "TEST POST" } });

    await waitFor(() => {
      const resultLink = screen.getByRole("link", { name: /test post 1/i });
      expect(resultLink).toBeInTheDocument();
    });
  });
});
