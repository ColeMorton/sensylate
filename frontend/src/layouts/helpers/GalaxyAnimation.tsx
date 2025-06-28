import React, { useEffect, useRef } from "react";
import * as THREE from "three";

// Make THREE available globally for debugging
if (typeof window !== "undefined") {
  (window as any).THREE = THREE;
}

// Inline configuration to avoid import issues during testing
const defaultConfig = {
  particles: {
    count: 100000, // Back to realistic count
    size: 0.05, // Optimized size for visibility
    sizeVariation: 0.5,
  },
  structure: {
    radius: 8,
    branches: 4,
    spin: 2.5,
    thickness: 0.3,
    coreRadius: 0.8,
    armWidth: 0.4,
  },
  distribution: {
    randomness: 0.3,
    randomnessPower: 3,
    clumpiness: 0.2,
  },
  colors: {
    core: "#00bcd4", // Cyan core
    inner: "#2196f3", // Blue inner
    outer: "#7e57c2", // Purple outer
    halo: "#3f51b5", // Deep purple halo
  },
  animation: {
    rotationSpeed: 0.02,
    particleSpeed: 0.001,
    enabled: true,
  },
  camera: {
    distance: 10, // Moved closer for better visibility
    angle: 23.6,
    fov: 50,
    lookAtOffset: 0, // Look at true center for proper positioning
  },
  performance: {
    pixelRatio: 1,
    antialias: true,
    shadows: false,
  },
};

interface GalaxyAnimationProps {
  className?: string;
  config?: any;
}

const GalaxyAnimation: React.FC<GalaxyAnimationProps> = ({
  className = "",
  config: customConfig,
}) => {
  // Deep merge configuration
  const config = customConfig
    ? {
        particles: { ...defaultConfig.particles, ...customConfig.particles },
        structure: { ...defaultConfig.structure, ...customConfig.structure },
        distribution: {
          ...defaultConfig.distribution,
          ...customConfig.distribution,
        },
        colors: { ...defaultConfig.colors, ...customConfig.colors },
        animation: { ...defaultConfig.animation, ...customConfig.animation },
        camera: { ...defaultConfig.camera, ...customConfig.camera },
        performance: {
          ...defaultConfig.performance,
          ...customConfig.performance,
        },
      }
    : defaultConfig;
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const sceneRef = useRef<{
    scene?: THREE.Scene;
    camera?: THREE.PerspectiveCamera;
    renderer?: THREE.WebGLRenderer;
    galaxy?: THREE.Points;
    animationId?: number;
    isInitialized?: boolean;
  }>({});

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    // Prevent double initialization
    if (sceneRef.current.isInitialized) {
      return;
    }

    const container = containerRef.current;
    const { current: refs } = sceneRef;

    // Mark as initializing
    refs.isInitialized = true;

    // Clean up any existing renderer first
    if (refs.renderer) {
      refs.renderer.dispose();
      if (canvasRef.current && container.contains(canvasRef.current)) {
        container.removeChild(canvasRef.current);
      }
      canvasRef.current = null;
    }

    // Scene setup
    refs.scene = new THREE.Scene();
    // Set background to transparent to inherit page background
    refs.scene.background = null;

    // Add some ambient light just in case
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    refs.scene.add(ambientLight);

    // Camera setup with container aspect ratio
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    refs.camera = new THREE.PerspectiveCamera(
      config.camera.fov,
      containerWidth / containerHeight,
      0.1,
      100,
    );
    // Position camera at configured angle
    const angle = (config.camera.angle * Math.PI) / 180; // Convert to radians
    const distance = config.camera.distance;
    const x = 0;
    const y = Math.sin(angle) * distance;
    const z = Math.cos(angle) * distance;
    refs.camera.position.set(x, y, z);
    // Look at galaxy center (0,0,0) with optional offset
    const targetY = config.camera.lookAtOffset;
    refs.camera.lookAt(0, targetY, 0);

    // Renderer setup with error handling
    try {
      // Create a new canvas element to avoid context conflicts
      const canvas = document.createElement("canvas");
      canvasRef.current = canvas;

      refs.renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: config.performance.antialias,
        alpha: true,
        powerPreference: "high-performance",
        preserveDrawingBuffer: true,
      });
      refs.renderer.setPixelRatio(
        window.devicePixelRatio * config.performance.pixelRatio,
      );

      // Set the renderer size to match container exactly
      refs.renderer.setSize(containerWidth, containerHeight);
      refs.renderer.setClearColor(0x000000, 0); // Transparent background

      // Canvas should automatically size to container, but ensure it's constrained
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.maxWidth = `${containerWidth}px`;
      canvas.style.maxHeight = `${containerHeight}px`;
      canvas.style.display = "block";

      container.appendChild(canvas);
    } catch (error) {
      console.error("GalaxyAnimation: Failed to create WebGL renderer:", error);
      return;
    }

    // Create galaxy
    const createGalaxy = () => {
      try {
        // Dispose previous galaxy
        if (refs.galaxy) {
          refs.galaxy.geometry.dispose();
          (refs.galaxy.material as THREE.Material).dispose();
          refs.scene!.remove(refs.galaxy);
        }

        // Geometry
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(config.particles.count * 3);
        const colors = new Float32Array(config.particles.count * 3);
        const sizes = new Float32Array(config.particles.count);

        // Color setup
        const colorCore = new THREE.Color(config.colors.core);
        const colorInner = new THREE.Color(config.colors.inner);
        const colorOuter = new THREE.Color(config.colors.outer);
        const colorHalo = new THREE.Color(config.colors.halo);

        for (let i = 0; i < config.particles.count; i++) {
          const i3 = i * 3;

          // Radius with concentration toward center
          let radius = Math.pow(Math.random(), 2) * config.structure.radius;

          // Branch calculation
          const branchIndex = i % config.structure.branches;
          const branchAngle =
            (branchIndex / config.structure.branches) * Math.PI * 2;
          const spinAngle = radius * config.structure.spin;

          // Arm width falloff - particles concentrate along spiral arms
          const armOffset = (Math.random() - 0.5) * config.structure.armWidth;
          const armFalloff =
            1 - Math.abs(armOffset) / config.structure.armWidth;

          // Enhanced randomness for realistic distribution
          const randomRadius = Math.pow(
            Math.random(),
            config.distribution.randomnessPower,
          );
          const randomAngle = Math.random() * Math.PI * 2;

          const randomX =
            Math.cos(randomAngle) *
            randomRadius *
            config.distribution.randomness *
            radius;
          const randomZ =
            Math.sin(randomAngle) *
            randomRadius *
            config.distribution.randomness *
            radius;

          // Vertical distribution (disk thickness)
          const thickness =
            config.structure.thickness * (1 - radius / config.structure.radius);
          const randomY = (Math.random() - 0.5) * thickness;

          // Core concentration
          if (radius < config.structure.coreRadius) {
            // Dense core region
            const coreRatio = radius / config.structure.coreRadius;
            radius *= 0.5 + 0.5 * coreRatio; // Compress core
            positions[i3] =
              Math.cos(branchAngle + spinAngle * 0.3) * radius + randomX * 0.5;
            positions[i3 + 1] = randomY * 0.5;
            positions[i3 + 2] =
              Math.sin(branchAngle + spinAngle * 0.3) * radius + randomZ * 0.5;
          } else {
            // Spiral arms
            const x = Math.cos(branchAngle + spinAngle) * radius;
            const z = Math.sin(branchAngle + spinAngle) * radius;

            // Apply arm offset perpendicular to spiral direction
            const perpX = -Math.sin(branchAngle + spinAngle) * armOffset;
            const perpZ = Math.cos(branchAngle + spinAngle) * armOffset;

            positions[i3] = x + perpX + randomX;
            positions[i3 + 1] = randomY;
            positions[i3 + 2] = z + perpZ + randomZ;
          }

          // Clumpiness - occasional dense regions
          if (Math.random() < config.distribution.clumpiness) {
            const clumpSize = 0.1 + Math.random() * 0.2;
            positions[i3] += (Math.random() - 0.5) * clumpSize;
            positions[i3 + 1] += (Math.random() - 0.5) * clumpSize * 0.5;
            positions[i3 + 2] += (Math.random() - 0.5) * clumpSize;
          }

          // Color gradient
          const normalizedRadius = radius / config.structure.radius;
          let finalColor = new THREE.Color();

          if (normalizedRadius < 0.3) {
            // Core region - cyan to blue gradient
            const t = normalizedRadius / 0.3;
            finalColor = colorCore.clone().lerp(colorInner, t);
          } else if (normalizedRadius < 0.7) {
            // Mid region - blue to purple gradient
            const t = (normalizedRadius - 0.3) / 0.4;
            finalColor = colorInner.clone().lerp(colorOuter, t);
          } else {
            // Outer region - purple to deep purple halo
            const t = (normalizedRadius - 0.7) / 0.3;
            finalColor = colorOuter.clone().lerp(colorHalo, t);
          }

          // Apply arm brightness - increased overall brightness
          finalColor.multiplyScalar(0.9 + 0.4 * armFalloff);

          colors[i3] = finalColor.r;
          colors[i3 + 1] = finalColor.g;
          colors[i3 + 2] = finalColor.b;

          // Size variation
          const baseSize = config.particles.size;
          const sizeVariation =
            1 + (Math.random() - 0.5) * config.particles.sizeVariation;

          // Smaller particles in outer regions
          const sizeFalloff = 1 - normalizedRadius * 0.5;

          // Brighter/larger particles in core
          const coreBrightness = normalizedRadius < 0.1 ? 3 : 1.5;

          sizes[i] = baseSize * sizeVariation * sizeFalloff * coreBrightness;
        }

        geometry.setAttribute(
          "position",
          new THREE.BufferAttribute(positions, 3),
        );
        geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
        geometry.setAttribute("size", new THREE.BufferAttribute(sizes, 1));

        // Vertex shader for size attribute
        const vertexShader = `
        attribute float size;
        varying vec3 vColor;

        void main() {
          vColor = color;
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          gl_PointSize = size * (300.0 / -mvPosition.z);
          gl_Position = projectionMatrix * mvPosition;
        }
      `;

        // Fragment shader
        const fragmentShader = `
        varying vec3 vColor;

        void main() {
          float dist = distance(gl_PointCoord, vec2(0.5));
          if (dist > 0.5) discard;

          float opacity = 1.0 - smoothstep(0.0, 0.5, dist);
          gl_FragColor = vec4(vColor, opacity);
        }
      `;

        // Material with custom shaders - try normal blending for debugging
        const material = new THREE.ShaderMaterial({
          uniforms: {},
          vertexShader,
          fragmentShader,
          blending: THREE.AdditiveBlending, // Back to additive for brightness
          depthWrite: false,
          transparent: true,
          vertexColors: true,
        });

        // Points
        refs.galaxy = new THREE.Points(geometry, material);

        // Position galaxy at origin - let camera positioning handle centering
        refs.galaxy.position.set(0, 0, 0);

        refs.scene!.add(refs.galaxy);
      } catch (error) {
        console.error("GalaxyAnimation: Failed to create galaxy:", error);
      }
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
      if (refs.galaxy && config.animation.enabled) {
        refs.galaxy.rotation.y = elapsedTime * config.animation.rotationSpeed;
      }

      if (refs.renderer && refs.scene && refs.camera) {
        refs.renderer.render(refs.scene, refs.camera);
      }
    };

    animate();

    // Handle resize
    const handleResize = () => {
      if (!container || !refs.camera || !refs.renderer || !canvasRef.current) {
        return;
      }

      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;

      refs.camera.aspect = containerWidth / containerHeight;
      refs.camera.updateProjectionMatrix();
      refs.renderer.setSize(containerWidth, containerHeight);

      // Update canvas style
      canvasRef.current.style.width = "100%";
      canvasRef.current.style.height = "100%";
      canvasRef.current.style.maxWidth = `${containerWidth}px`;
      canvasRef.current.style.maxHeight = `${containerHeight}px`;
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
        if (canvasRef.current && container.contains(canvasRef.current)) {
          container.removeChild(canvasRef.current);
        }
        canvasRef.current = null;
      }

      // Reset initialization flag
      refs.isInitialized = false;
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
