import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-semibold mb-4">AMM SaaS Demo Frontend</h1>
      <Link href="/login" className="text-blue-600 underline">
        Se connecter
      </Link>
    </div>
  );
}
