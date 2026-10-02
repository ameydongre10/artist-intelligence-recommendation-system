import { HirerDetailClient } from './HirerDetailClient';

const BRIEF_IDS = [
  '01_cafe_music_whatsapp',
  '02_skincare_photography_chat',
  '03_vertical_video_email',
  '04_leadership_event_photos',
];

export function generateStaticParams() {
  return BRIEF_IDS.map((id) => ({ id }));
}

export default function HirerDetailPage({ params }: { params: { id: string } }) {
  return <HirerDetailClient initialId={params?.id} />;
}
