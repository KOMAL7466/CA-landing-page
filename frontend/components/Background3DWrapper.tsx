'use client';
import dynamic from 'next/dynamic';

const Background3D = dynamic(() => import('@/components/Background3D'), { ssr: false });

export default function Background3DWrapper() {
  return <Background3D />;
}