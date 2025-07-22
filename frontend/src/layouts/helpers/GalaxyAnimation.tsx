import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { getThemeColors } from "@/utils/chartTheme";

interface GalaxyAnimationProps {
  className?: string;
}

const GalaxyAnimation: React.FC<GalaxyAnimationProps> = ({
  className = "",
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<{
    scene?: THREE.Scene;
    camera?: THREE.PerspectiveCamera;
    renderer?: THREE.WebGLRenderer;
    galaxy?: THREE.Points;
    animationId?: number;
  }>({});

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const container = containerRef.current;
    const { current: refs } = sceneRef;

    // Scene setup
    refs.scene = new THREE.Scene();
    // Set background to transparent to inherit page background
    refs.scene.background = null;

    // Camera setup
    refs.camera = new THREE.PerspectiveCamera(
      50,
      container.clientWidth / container.clientHeight,
      0.1,
      100,
    );
    // Position camera at 23.6 degrees above horizontal
    const angle = (23.6 * Math.PI) / 180; // Convert to radians
    const distance = 8;
    const x = 0;
    const y = Math.sin(angle) * distance;
    const z = Math.cos(angle) * distance;
    refs.camera.position.set(x, y, z);
    // Look at a point below galaxy center to raise it on screen
    const targetY = -y * 0.4; // Look below center to raise galaxy visually
    refs.camera.lookAt(0, targetY, 0);

    // Renderer setup
    refs.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    refs.renderer.setPixelRatio(window.devicePixelRatio);
    refs.renderer.setSize(container.clientWidth, container.clientHeight);
    refs.renderer.setClearColor(0x000000, 0); // Transparent background
    container.appendChild(refs.renderer.domElement);

    // Detect theme mode
    const isDarkMode = document.documentElement.classList.contains("dark");
    const themeColors = getThemeColors(isDarkMode);

    // Galaxy parameters
    const parameters = {
      count: 20000,
      size: 0.08,
      radius: 5,
      branches: 3,
      spin: 1,
      randomness: 0.2,
      randomnessPower: 3,
      insideColor: themeColors.primaryData, // Primary data color for inner core
      neutralColor: themeColors.tertiaryData, // Neutral data color for middle
      outsideColor: themeColors.secondaryData, // Secondary data color for outer edges
    };

    // Create galaxy
    const createGalaxy = () => {
      // Dispose previous galaxy
      if (refs.galaxy) {
        refs.galaxy.geometry.dispose();
        (refs.galaxy.material as THREE.Material).dispose();
        refs.scene!.remove(refs.galaxy);
      }

      // Geometry
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(parameters.count * 3);
      const colors = new Float32Array(parameters.count * 3);

      const colorInside = new THREE.Color(parameters.insideColor);
      const colorNeutral = new THREE.Color(parameters.neutralColor);
      const colorOutside = new THREE.Color(parameters.outsideColor);

      for (let i = 0; i < parameters.count; i++) {
        const i3 = i * 3;

        // Position
        const radius = Math.random() * parameters.radius;
        const branchAngle =
          ((i % parameters.branches) / parameters.branches) * Math.PI * 2;
        const spinAngle = radius * parameters.spin;

        const randomX =
          Math.pow(Math.random(), parameters.randomnessPower) *
          (Math.random() < 0.5 ? 1 : -1) *
          parameters.randomness *
          radius;
        const randomY =
          Math.pow(Math.random(), parameters.randomnessPower) *
          (Math.random() < 0.5 ? 1 : -1) *
          parameters.randomness *
          radius;
        const randomZ =
          Math.pow(Math.random(), parameters.randomnessPower) *
          (Math.random() < 0.5 ? 1 : -1) *
          parameters.randomness *
          radius;

        positions[i3] = Math.cos(branchAngle + spinAngle) * radius + randomX;
        positions[i3 + 1] = randomY;
        positions[i3 + 2] =
          Math.sin(branchAngle + spinAngle) * radius + randomZ;

        // Color - Three-color gradient: primary_data → neutral_data → secondary_data
        const normalizedRadius = radius / parameters.radius;
        let mixedColor;

        if (normalizedRadius <= 0.5) {
          // Inner segment: primary_data to neutral_data
          const innerLerpFactor = normalizedRadius * 2; // Scale 0-0.5 to 0-1
          mixedColor = colorInside.clone();
          mixedColor.lerp(colorNeutral, innerLerpFactor);
        } else {
          // Outer segment: neutral_data to secondary_data
          const outerLerpFactor = (normalizedRadius - 0.5) * 2; // Scale 0.5-1 to 0-1
          mixedColor = colorNeutral.clone();
          mixedColor.lerp(colorOutside, outerLerpFactor);
        }

        colors[i3] = mixedColor.r;
        colors[i3 + 1] = mixedColor.g;
        colors[i3 + 2] = mixedColor.b;
      }

      geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(positions, 3),
      );
      geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

      // Material
      const material = new THREE.PointsMaterial({
        size: parameters.size,
        sizeAttenuation: true,
        depthWrite: false,
        blending: THREE.NormalBlending,
        vertexColors: true,
      });

      // Points
      refs.galaxy = new THREE.Points(geometry, material);
      refs.scene!.add(refs.galaxy);
    };

    createGalaxy();

    // Theme change detection function
    const handleThemeChange = () => {
      if (!refs.galaxy) {
        return;
      }

      // Update blending mode without recreating the galaxy
      const material = refs.galaxy.material as THREE.PointsMaterial;
      material.blending = THREE.NormalBlending;
      material.needsUpdate = true;
    };

    // Multiple listeners for theme changes
    const themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === "attributes" &&
          mutation.attributeName === "class"
        ) {
          // Add a small delay to ensure the DOM has updated
          setTimeout(handleThemeChange, 10);
        }
      });
    });

    // Observe changes to the document element's class attribute
    themeObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });

    // Listen for storage changes (theme switcher uses localStorage)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "theme") {
        setTimeout(handleThemeChange, 10);
      }
    };
    window.addEventListener("storage", handleStorageChange);

    // Listen for click events on theme switcher
    const handleThemeClick = (e: Event) => {
      const target = e.target as HTMLElement;
      if (
        target.matches("[data-theme-switcher]") ||
        target.closest("[data-theme-switcher]")
      ) {
        setTimeout(handleThemeChange, 100);
      }
    };
    document.addEventListener("click", handleThemeClick);

    // Animation loop
    const clock = new THREE.Clock();

    const animate = () => {
      refs.animationId = requestAnimationFrame(animate);

      const elapsedTime = clock.getElapsedTime();

      // Rotate galaxy
      if (refs.galaxy) {
        refs.galaxy.rotation.y = elapsedTime * 0.1;
      }

      refs.renderer!.render(refs.scene!, refs.camera!);
    };

    animate();

    // Handle resize
    const handleResize = () => {
      if (!container || !refs.camera || !refs.renderer) {
        return;
      }

      refs.camera.aspect = container.clientWidth / container.clientHeight;
      refs.camera.updateProjectionMatrix();
      refs.renderer.setSize(container.clientWidth, container.clientHeight);
    };

    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => {
      if (refs.animationId) {
        cancelAnimationFrame(refs.animationId);
      }

      window.removeEventListener("resize", handleResize);
      window.removeEventListener("storage", handleStorageChange);
      document.removeEventListener("click", handleThemeClick);
      themeObserver.disconnect();

      if (refs.galaxy) {
        refs.galaxy.geometry.dispose();
        (refs.galaxy.material as THREE.Material).dispose();
      }

      if (refs.renderer) {
        refs.renderer.dispose();
        if (container.contains(refs.renderer.domElement)) {
          container.removeChild(refs.renderer.domElement);
        }
      }
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className={`h-full w-full ${className}`}
      style={{ minHeight: "100vh" }}
    />
  );
};

export default GalaxyAnimation;
