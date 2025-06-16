import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchModal from "../layouts/helpers/SearchModal";

describe("SearchModal", () => {
  beforeEach(() => {
    // Reset DOM before each test
    document.body.innerHTML = "";
  });

  it("renders search modal correctly", () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);
    expect(searchInput).toBeInTheDocument();
  });

  it("handles search input changes", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "test" } });

    expect(searchInput).toHaveValue("test");
  });

  it("filters search results based on title", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "test post 1" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });

  it("filters search results based on description", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

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

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "technology" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });

  it("filters search results based on tags", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "astro" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });

  it("shows no results when search string does not match", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "nonexistent content" } });

    await waitFor(() => {
      const noResults = screen.getByText(/no search found/i);
      expect(noResults).toBeInTheDocument();
    });
  });

  it("shows empty state when search string is empty", () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "" } });

    // Should not show any results or "no results" message
    expect(screen.queryByText(/no search found/i)).not.toBeInTheDocument();
  });

  it("handles special characters in search input", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    // Test backslash handling (as seen in the component code)
    fireEvent.change(searchInput, { target: { value: "test\\post" } });

    expect(searchInput).toHaveValue("testpost"); // Backslash should be removed
  });

  it("performs case-insensitive search", async () => {
    render(<SearchModal />);

    const searchInput = screen.getByPlaceholderText(/search here/i);

    fireEvent.change(searchInput, { target: { value: "TEST POST" } });

    await waitFor(() => {
      const results = screen.getByText("Test Post 1");
      expect(results).toBeInTheDocument();
    });
  });
});
