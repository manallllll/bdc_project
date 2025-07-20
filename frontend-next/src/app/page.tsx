'use client';

import { useEffect, useState } from 'react';
import SearchBar from '@/components/SearchBar';
import Filters from '@/components/Filters';
import Sidebar from '@/components/Sidebar';
import DashboardCard from '@/components/DashboardCard';
import Chart from '@/components/Chart';

interface AoData {
  _id: string;
  url: string;
  titre: string;
  date_publication: string;
  description: string;
  fichier: string;
}

interface BdcData {
  date_mise_en_ligne: string;
  quantite: number;
}

export default function HomePage() {
  const [aos, setAos] = useState<AoData[]>([]);
  const [bdcs, setBdcs] = useState<BdcData[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({ region: '', secteur: '' });

  useEffect(() => {
    const fetchAos = async () => {
      const res = await fetch('/api/ao');
      const data = await res.json();
      // ✅ Adaptateur pour éviter les erreurs de typage
      const formatted = data.map((ao: any) => ({
        _id: ao._id ?? '',
        url: ao.url ?? '',
        titre: ao.titre ?? '',
        date_publication: ao.date_publication ?? '',
        description: ao.description ?? '',
        fichier: ao.fichier ?? '',
      }));
      setAos(formatted);
    };

    const fetchBdcs = async () => {
      const res = await fetch('/api/bdc');
      const data = await res.json();
      const formatted = data.map((bdc: any) => ({
        date_mise_en_ligne: bdc.date_mise_en_ligne ?? '',
        quantite: bdc.articles?.[0]?.quantite ?? 0,
      }));
      setBdcs(formatted);
    };

    fetchAos();
    fetchBdcs();
  }, []);

  const filteredAos = aos.filter(ao =>
    ao.titre.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredBdcs = bdcs.filter(bdc => {
    // Ajoute ici une logique de filtre si nécessaire
    return true;
  });

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6 bg-gray-50">
        <SearchBar onSearch={(q) => setSearchQuery(q)} />
        <Filters onFilter={(f) => setFilters(f)} />
        <DashboardCard data={filteredAos} />
        <Chart data={filteredBdcs} />
      </main>
    </div>
  );
}
