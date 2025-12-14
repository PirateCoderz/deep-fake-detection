import { Metadata } from 'next';
import HomePage from '@/components/pages/HomePage';

export const metadata: Metadata = {
  title: 'Upload Image - Fake Product Detection',
  description: 'Upload a product image to verify its authenticity',
};

export default function Page() {
  return <HomePage />;
}
