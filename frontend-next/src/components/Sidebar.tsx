'use client';
import Link from 'next/link';

export default function Sidebar() {
  return (
    <aside className="h-screen w-64 bg-white shadow-md p-5 fixed top-0 left-0">
      <h2 className="text-xl font-bold mb-8 text-center">BDC Platform</h2>
      <nav className="flex flex-col gap-4">
        <Link href="/" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
        <Link href="/bdc" className="text-gray-700 hover:text-blue-600">Bons de Commande</Link>
        <Link href="/ao" className="text-gray-700 hover:text-blue-600">Appels d’Offres</Link>
        <Link href="/logout" className="text-red-500 hover:text-red-700 mt-12">Déconnexion</Link>
      </nav>
    </aside>
  );
}
