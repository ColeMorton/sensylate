import React from "react";
import { IconCircleCheck, IconCircleX } from "@tabler/icons-react";

interface ProsConsProps {
  pros: string[];
  cons: string[];
  className?: string;
}

const ProsCons: React.FC<ProsConsProps> = ({ pros, cons, className = "" }) => {
  return (
    <div className={`space-y-4 ${className}`}>
      {/* Pros Section */}
      <div>
        <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold tracking-wider text-gray-700 uppercase dark:text-gray-300">
          <IconCircleCheck size={18} className="text-green-500" />
          Pros
        </h4>
        <ul className="space-y-2">
          {pros.map((pro, index) => (
            <li
              key={index}
              className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300"
            >
              <IconCircleCheck
                size={16}
                className="mt-0.5 flex-shrink-0 text-green-500"
              />
              <span>{pro}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Cons Section */}
      <div>
        <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold tracking-wider text-gray-700 uppercase dark:text-gray-300">
          <IconCircleX size={18} className="text-red-500" />
          Cons
        </h4>
        <ul className="space-y-2">
          {cons.map((con, index) => (
            <li
              key={index}
              className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300"
            >
              <IconCircleX
                size={16}
                className="mt-0.5 flex-shrink-0 text-red-500"
              />
              <span>{con}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ProsCons;
