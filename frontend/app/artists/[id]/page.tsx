import { ArtistDetailClient } from './ArtistDetailClient';

const ARTIST_IDS = [
  'P01', 'P02', 'P03', 'PO4', 'PO5',
  'M01', 'M02', 'M03', 'M04', 'M05',
  'V01', 'V02', 'V03', 'VO4', 'VO5',
];

export function generateStaticParams() {
  return ARTIST_IDS.map((id) => ({ id }));
}

export default function ArtistDetailPage({ params }: { params: { id: string } }) {
  return <ArtistDetailClient initialId={params?.id} />;
}
