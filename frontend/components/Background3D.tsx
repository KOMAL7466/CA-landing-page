'use client';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sphere, MeshDistortMaterial } from '@react-three/drei';

export default function Background3D() {
  return (
    <div className="fixed top-0 left-0 w-full h-full -z-10">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} />
        <Sphere args={[1, 100, 200]} scale={2}>
          <MeshDistortMaterial color="#3b82f6" attach="material" distort={0.4} speed={1.5} />
        </Sphere>
        <OrbitControls enableZoom={false} autoRotate rotateSpeed={0.5} />
      </Canvas>
    </div>
  );
}