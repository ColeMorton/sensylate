export type Feature = {
  button: Button;
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
  themeSwitcher: boolean;
  comments: boolean;
  gtm: boolean;
  calculators: boolean;
  calculatorAdvanced: boolean;
  elementsPage: boolean;
  authorsPage: boolean;
  chartsPage: boolean;
}

// Configuration Types
export interface SiteConfig {
  title: string;
  base_url: string;
  base_path: string;
  trailing_slash: boolean;
  favicon: string;
  logo: string;
  logo_darkmode: string;
  logo_width: string;
  logo_height: string;
  logo_text: string;
}

export interface SettingsConfig {
  search: boolean;
  sticky_header: boolean;
  theme_switcher: boolean;
  default_theme: string;
  pagination: number;
  summary_length: number;
  blog_folder: string;
}

export interface ParamsConfig {
  contact_form_action: string;
  copyright: string;
}

export interface NavigationButtonConfig {
  enable: boolean;
  label: string;
  link: string;
}

export interface GoogleTagManagerConfig {
  enable: boolean;
  gtm_id: string;
}

export interface DisqusConfig {
  enable: boolean;
  shortname: string;
  settings: Record<string, unknown>;
}

export interface MetadataConfig {
  meta_author: string;
  meta_image: string;
  meta_description: string;
}

export interface EnhancedConfig {
  features: FeatureFlags;
  site: SiteConfig;
  settings: SettingsConfig;
  params: ParamsConfig;
  navigation_button: NavigationButtonConfig;
  google_tag_manager: GoogleTagManagerConfig;
  disqus: DisqusConfig;
  metadata: MetadataConfig;
}
