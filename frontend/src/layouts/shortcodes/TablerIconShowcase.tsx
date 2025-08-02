import React, { useState } from "react";
import * as TablerIcons from "@tabler/icons-react";

const {
  IconHome,
  IconSettings,
  IconUser,
  IconMail,
  IconPhone,
  IconDownload,
  IconUpload,
  IconSearch,
  IconBell,
  IconHeart,
  IconStar,
  IconShare,
  IconTrash,
  IconEdit,
  IconPlus,
  IconMinus,
  IconCheck,
  IconX,
  IconArrowLeft,
  IconArrowRight,
  IconArrowUp,
  IconArrowDown,
  IconCalendar,
  IconClock,
  IconFile,
  IconFolder,
  IconCamera,
  IconPhoto,
  IconVideo,
  IconMusic,
  IconShoppingCart,
  IconCreditCard,
  IconGift,
  IconLocation,
  IconMap,
  IconSun,
  IconMoon,
  IconCloud,
  IconDatabase,
  IconServer,
  IconCode,
  IconTerminal,
  IconBrandGithub,
  IconBrandTwitter,
  IconBrandLinkedin,
  IconEye,
  IconEyeOff,
  IconLock,
  IconLockOpen,
} = TablerIcons;

interface IconData {
  name: string;
  component: React.ComponentType<{ size?: number; className?: string }>;
  description: string;
}

const popularIcons: IconData[] = [
  { name: "IconHome", component: IconHome, description: "Home" },
  { name: "IconSettings", component: IconSettings, description: "Settings" },
  { name: "IconUser", component: IconUser, description: "User" },
  { name: "IconMail", component: IconMail, description: "Mail" },
  { name: "IconPhone", component: IconPhone, description: "Phone" },
  { name: "IconDownload", component: IconDownload, description: "Download" },
  { name: "IconUpload", component: IconUpload, description: "Upload" },
  { name: "IconSearch", component: IconSearch, description: "Search" },
  { name: "IconBell", component: IconBell, description: "Notifications" },
  { name: "IconHeart", component: IconHeart, description: "Heart" },
  { name: "IconStar", component: IconStar, description: "Star" },
  { name: "IconShare", component: IconShare, description: "Share" },
  { name: "IconTrash", component: IconTrash, description: "Delete" },
  { name: "IconEdit", component: IconEdit, description: "Edit" },
  { name: "IconPlus", component: IconPlus, description: "Add" },
  { name: "IconMinus", component: IconMinus, description: "Remove" },
  { name: "IconCheck", component: IconCheck, description: "Check" },
  { name: "IconX", component: IconX, description: "Close" },
  {
    name: "IconArrowLeft",
    component: IconArrowLeft,
    description: "Arrow Left",
  },
  {
    name: "IconArrowRight",
    component: IconArrowRight,
    description: "Arrow Right",
  },
  { name: "IconArrowUp", component: IconArrowUp, description: "Arrow Up" },
  {
    name: "IconArrowDown",
    component: IconArrowDown,
    description: "Arrow Down",
  },
  { name: "IconCalendar", component: IconCalendar, description: "Calendar" },
  { name: "IconClock", component: IconClock, description: "Time" },
  { name: "IconFile", component: IconFile, description: "File" },
  { name: "IconFolder", component: IconFolder, description: "Folder" },
  { name: "IconCamera", component: IconCamera, description: "Camera" },
  { name: "IconPhoto", component: IconPhoto, description: "Photo" },
  { name: "IconVideo", component: IconVideo, description: "Video" },
  { name: "IconMusic", component: IconMusic, description: "Music" },
  {
    name: "IconShoppingCart",
    component: IconShoppingCart,
    description: "Cart",
  },
  { name: "IconCreditCard", component: IconCreditCard, description: "Payment" },
  { name: "IconGift", component: IconGift, description: "Gift" },
  { name: "IconLocation", component: IconLocation, description: "Location" },
  { name: "IconMap", component: IconMap, description: "Map" },
  { name: "IconSun", component: IconSun, description: "Light Theme" },
  { name: "IconMoon", component: IconMoon, description: "Dark Theme" },
  { name: "IconCloud", component: IconCloud, description: "Cloud" },
  { name: "IconDatabase", component: IconDatabase, description: "Database" },
  { name: "IconServer", component: IconServer, description: "Server" },
  { name: "IconCode", component: IconCode, description: "Code" },
  { name: "IconTerminal", component: IconTerminal, description: "Terminal" },
  {
    name: "IconBrandGithub",
    component: IconBrandGithub,
    description: "GitHub",
  },
  {
    name: "IconBrandTwitter",
    component: IconBrandTwitter,
    description: "Twitter",
  },
  {
    name: "IconBrandLinkedin",
    component: IconBrandLinkedin,
    description: "LinkedIn",
  },
  { name: "IconEye", component: IconEye, description: "Show" },
  { name: "IconEyeOff", component: IconEyeOff, description: "Hide" },
  { name: "IconLock", component: IconLock, description: "Lock" },
  { name: "IconLockOpen", component: IconLockOpen, description: "Unlock" },
];

const TablerIconShowcase: React.FC = () => {
  const [copiedIcon, setCopiedIcon] = useState<string | null>(null);

  // Validate that all icons are properly loaded (development only)
  React.useEffect(() => {
    if (process.env.NODE_ENV === "development") {
      const undefinedIcons = popularIcons.filter((icon) => !icon.component);
      if (undefinedIcons.length > 0) {
        // TablerIconShowcase: Found undefined icons
      }
    }
  }, []);

  const copyToClipboard = async (iconName: string) => {
    try {
      await navigator.clipboard.writeText(iconName);
      setCopiedIcon(iconName);
      setTimeout(() => setCopiedIcon(null), 2000);
    } catch {
      // Fallback for browsers that don't support clipboard API
      // User feedback would be handled by showing copy was unsuccessful
    }
  };

  return (
    <div className="tabler-icon-showcase">
      <div className="mb-6">
        <h3 className="mb-2 text-xl font-semibold">Tabler Icons</h3>
        <p className="mb-4 text-gray-600 dark:text-gray-400">
          Click on any icon to copy its component name to clipboard. All icons
          support customization via props like size, color, and stroke.
        </p>
      </div>

      <div className="mb-8 grid grid-cols-4 gap-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10">
        {popularIcons.map((iconData) => {
          const IconComponent = iconData.component;
          const isCopied = copiedIcon === iconData.name;

          return (
            <div
              key={iconData.name}
              className={`group hover:border-primary hover:bg-primary/5 dark:hover:bg-primary/10 relative cursor-pointer rounded-lg border p-3 transition-all duration-200 ${isCopied ? "border-green-500 bg-green-50 dark:bg-green-900/20" : "border-gray-200 dark:border-gray-700"} `}
              onClick={() => copyToClipboard(iconData.name)}
              title={`${iconData.description} - Click to copy`}
            >
              <div className="flex flex-col items-center">
                <IconComponent
                  size={24}
                  className={`transition-colors duration-200 ${isCopied ? "text-green-600" : "group-hover:text-primary text-gray-700 dark:text-gray-300"} `}
                />
                <span className="mt-2 w-full truncate text-center text-xs text-gray-600 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-gray-200">
                  {iconData.description}
                </span>
              </div>

              {isCopied && (
                <div className="absolute -top-2 -right-2 rounded-full bg-green-500 px-2 py-1 text-xs text-white">
                  ✓
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="mt-8 rounded-lg bg-gray-50 p-6 dark:bg-gray-800">
        <h4 className="mb-3 text-lg font-semibold">Usage Examples</h4>

        <div className="space-y-4">
          <div>
            <h5 className="mb-2 font-medium">Direct Import:</h5>
            <pre className="overflow-x-auto rounded border bg-white p-3 text-sm dark:bg-gray-900">
              <code>{`import { IconHome, IconUser } from "@tabler/icons-react";

function MyComponent() {
  return (
    <div>
      <IconHome size={24} />
      <IconUser size={32} color="#blue" />
    </div>
  );
}`}</code>
            </pre>
          </div>

          <div>
            <h5 className="mb-2 font-medium">Via DynamicIcon Helper:</h5>
            <pre className="overflow-x-auto rounded border bg-white p-3 text-sm dark:bg-gray-900">
              <code>{`import DynamicIcon from "@/helpers/DynamicIcon";

function MyComponent() {
  return (
    <div>
      <DynamicIcon icon="TbIconHome" className="w-6 h-6" />
      <DynamicIcon icon="TbIconUser" className="w-8 h-8 text-blue-500" />
    </div>
  );
}`}</code>
            </pre>
          </div>
        </div>

        <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
          <p>
            <strong>Note:</strong> For DynamicIcon, use the "Tb" prefix followed
            by the full icon name (e.g., "TbIconHome" for IconHome).
          </p>
        </div>
      </div>
    </div>
  );
};

export default TablerIconShowcase;
