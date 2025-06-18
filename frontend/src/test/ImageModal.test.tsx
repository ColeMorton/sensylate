import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import ImageModal from "@/layouts/helpers/ImageModal";
import * as useFeatureFlagModule from "@/hooks/useFeatureFlag";

// Mock the useFeatureFlag hook
vi.mock("@/hooks/useFeatureFlag", () => ({
  useFeatureFlag: vi.fn(),
}));

describe("ImageModal", () => {
  const mockOnClose = vi.fn();
  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
    imageSrc: "/test-image.jpg",
    imageAlt: "Test image",
    imageSrcSet: "/test-image@2x.jpg 2x",
  };

  beforeEach(() => {
    // Mock useFeatureFlag to return true by default
    vi.mocked(useFeatureFlagModule.useFeatureFlag).mockReturnValue(true);

    // Reset mocks
    mockOnClose.mockClear();

    // Mock body style
    document.body.style.overflow = "";
  });

  afterEach(() => {
    // Clean up
    document.body.style.overflow = "";
  });

  it("renders when isOpen is true and feature flag is enabled", () => {
    render(<ImageModal {...defaultProps} />);

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByAltText("Test image")).toBeInTheDocument();
    expect(screen.getByLabelText("Close image")).toBeInTheDocument();
  });

  it("does not render when isOpen is false", () => {
    render(<ImageModal {...defaultProps} isOpen={false} />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("does not render when feature flag is disabled", () => {
    vi.mocked(useFeatureFlagModule.useFeatureFlag).mockReturnValue(false);

    render(<ImageModal {...defaultProps} />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("calls onClose when escape key is pressed", () => {
    render(<ImageModal {...defaultProps} />);

    fireEvent.keyDown(document, { key: "Escape" });

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when close button is clicked", () => {
    render(<ImageModal {...defaultProps} />);

    const closeButton = screen.getByLabelText("Close image");
    fireEvent.click(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when clicking outside the image", () => {
    render(<ImageModal {...defaultProps} />);

    const modal = screen.getByRole("dialog");
    fireEvent.click(modal);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("does not call onClose when clicking on the image", () => {
    render(<ImageModal {...defaultProps} />);

    const image = screen.getByAltText("Test image");
    fireEvent.click(image);

    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it("sets body overflow to hidden when modal is open", async () => {
    render(<ImageModal {...defaultProps} />);

    await waitFor(() => {
      expect(document.body.style.overflow).toBe("hidden");
    });
  });

  it("resets body overflow when modal is closed", async () => {
    const { rerender } = render(<ImageModal {...defaultProps} />);

    // Modal is open, body overflow should be hidden
    await waitFor(() => {
      expect(document.body.style.overflow).toBe("hidden");
    });

    // Close modal
    rerender(<ImageModal {...defaultProps} isOpen={false} />);

    await waitFor(() => {
      expect(document.body.style.overflow).toBe("");
    });
  });

  it("renders image with correct src and srcSet", () => {
    render(<ImageModal {...defaultProps} />);

    const image = screen.getByAltText("Test image");
    expect(image).toHaveAttribute("src", "/test-image.jpg");
    expect(image).toHaveAttribute("srcset", "/test-image@2x.jpg 2x");
  });

  it("has proper accessibility attributes", () => {
    render(<ImageModal {...defaultProps} />);

    const modal = screen.getByRole("dialog");
    expect(modal).toHaveAttribute("aria-modal", "true");
    expect(modal).toHaveAttribute("aria-label", "Expanded image view");
    expect(modal).toHaveAttribute("tabIndex", "-1");
  });

  it("focuses on modal when opened", async () => {
    render(<ImageModal {...defaultProps} />);

    const modal = screen.getByRole("dialog");
    await waitFor(() => {
      expect(modal).toHaveFocus();
    });
  });

  it("handles keyboard events only when modal is open", () => {
    const { rerender } = render(
      <ImageModal {...defaultProps} isOpen={false} />,
    );

    // Should not respond to escape when closed
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).not.toHaveBeenCalled();

    // Open modal
    rerender(<ImageModal {...defaultProps} isOpen={true} />);

    // Should respond to escape when open
    fireEvent.keyDown(document, { key: "Escape" });
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });
});
