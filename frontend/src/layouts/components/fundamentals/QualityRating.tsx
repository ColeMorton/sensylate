import React from "react";
import { IconStar, IconStarFilled } from "@tabler/icons-react";

interface QualityRatingProps {
  category: string;
  rating: number;
  maxRating?: number;
  showValue?: boolean;
  className?: string;
}

const QualityRating: React.FC<QualityRatingProps> = ({
  category,
  rating,
  maxRating = 5,
  showValue = true,
  className = "",
}) => {
  const renderStars = () => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < maxRating; i++) {
      if (i < fullStars) {
        stars.push(
          <IconStarFilled
            key={i}
            size={20}
            className="text-yellow-400 dark:text-yellow-300"
          />,
        );
      } else if (i === fullStars && hasHalfStar) {
        // Half star implementation
        stars.push(
          <div key={i} className="relative">
            <IconStar size={20} className="text-gray-300 dark:text-gray-600" />
            <div
              className="absolute top-0 left-0 overflow-hidden"
              style={{ width: "50%" }}
            >
              <IconStarFilled
                size={20}
                className="text-yellow-400 dark:text-yellow-300"
              />
            </div>
          </div>,
        );
      } else {
        stars.push(
          <IconStar
            key={i}
            size={20}
            className="text-gray-300 dark:text-gray-600"
          />,
        );
      }
    }

    return stars;
  };

  return (
    <div className={`flex items-center justify-between py-2 ${className}`}>
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
        {category}
      </span>
      <div className="flex items-center gap-1">
        <div className="flex">{renderStars()}</div>
        {showValue && (
          <span className="ml-2 text-sm font-bold text-gray-900 dark:text-gray-100">
            {rating.toFixed(1)}
          </span>
        )}
      </div>
    </div>
  );
};

export default QualityRating;
