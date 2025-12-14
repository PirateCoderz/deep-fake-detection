import { Metadata } from 'next';
import ResultsPage from '@/components/pages/ResultsPage';

export const metadata: Metadata = {
  title: 'Classification Results - Fake Product Detection',
  description: 'View product authenticity classification results',
};

interface PageProps {
  params: {
    id: string;
  };
}

export default function Page({ params }: PageProps) {
  return <ResultsPage requestId={params.id} />;
}
