import React, { useEffect, useRef } from "react";
import * as THREE from "three";

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
    refs.scene.background = new THREE.Color(0x201919);

    // Camera setup
    refs.camera = new THREE.PerspectiveCamera(
      50,
      container.clientWidth / container.clientHeight,
      0.1,
      100,
    );
    refs.camera.position.set(4, 2, 5);

    // Renderer setup
    refs.renderer = new THREE.WebGLRenderer({ antialias: true });
    refs.renderer.setPixelRatio(window.devicePixelRatio);
    refs.renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(refs.renderer.domElement);

    // Galaxy parameters
    const parameters = {
      count: 20000,
      size: 0.08,
      radius: 5,
      branches: 3,
      spin: 1,
      randomness: 0.2,
      randomnessPower: 3,
      insideColor: "#ffa575",
      outsideColor: "#311599",
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

        // Color
        const mixedColor = colorInside.clone();
        mixedColor.lerp(colorOutside, radius / parameters.radius);

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
        blending: THREE.AdditiveBlending,
        vertexColors: true,
      });

      // Points
      refs.galaxy = new THREE.Points(geometry, material);
      refs.scene!.add(refs.galaxy);
    };

    createGalaxy();

    // Mouse controls
    let mouseX = 0;
    let mouseY = 0;
    let targetRotationX = 0;
    let targetRotationY = 0;

    const onMouseMove = (event: MouseEvent) => {
      mouseX =
        (event.clientX - container.clientWidth / 2) / container.clientWidth;
      mouseY =
        (event.clientY - container.clientHeight / 2) / container.clientHeight;
      targetRotationX = mouseY * 0.5;
      targetRotationY = mouseX * 0.5;
    };

    container.addEventListener("mousemove", onMouseMove);

    // Animation loop
    const clock = new THREE.Clock();

    const animate = () => {
      refs.animationId = requestAnimationFrame(animate);

      const elapsedTime = clock.getElapsedTime();

      // Rotate galaxy
      if (refs.galaxy) {
        refs.galaxy.rotation.y = elapsedTime * 0.1;

        // Smooth camera movement based on mouse
        refs.camera!.position.x +=
          (targetRotationY * 10 - refs.camera!.position.x) * 0.02;
        refs.camera!.position.y +=
          (targetRotationX * 10 - refs.camera!.position.y) * 0.02;
        refs.camera!.lookAt(refs.scene!.position);
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
      container.removeEventListener("mousemove", onMouseMove);

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
      className={`w-full h-full ${className}`}
      style={{ minHeight: "100vh" }}
    />
  );
};

export default GalaxyAnimation;
