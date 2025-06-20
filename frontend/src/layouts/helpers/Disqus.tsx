import config from "@/config/config.json";
import { features } from "@/lib/featureFlags";
import { DiscussionEmbed } from "disqus-react";
import React from "react";

const Disqus = ({ className }: { className?: string }) => {
  const { disqus } = config;
  return (
    <div className={className}>
      {features.comments && disqus.enable && (
        <DiscussionEmbed
          shortname={disqus.shortname}
          config={disqus.settings}
        />
      )}
    </div>
  );
};

export default Disqus;
