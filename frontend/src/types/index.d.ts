export type Feature = {
  button: button;
  image: string;
  bulletpoints: string[];
  content: string;
  title: string;
};

export type Button = {
  enable: boolean;
  label: string;
  link: string;
};

// Feature Flag Types
export interface FeatureFlags {
  search: boolean;
  theme_switcher: boolean;
  comments: boolean;
  gtm: boolean;
  calculator_advanced: boolean;
  elements_page: boolean;
}

export interface EnhancedConfig {
  features: FeatureFlags;
  site: any;
  settings: any;
  params: any;
  navigation_button: any;
  google_tag_manager: any;
  disqus: any;
  metadata: any;
}
