import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Background3DWrapper from '@/components/Background3DWrapper'; 

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CA AI Assistant',
  description: 'Your intelligent financial advisor',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} text-white`} suppressHydrationWarning>
        <Background3DWrapper /> {/* <-- use wrapper */}
        <main className="relative z-10 container mx-auto px-4 py-8">
          {children}
        </main>
    
      </body>
    </html>
  );
}