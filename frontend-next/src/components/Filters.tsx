"use client";

import React, { useEffect, useState } from "react";

interface FiltersProps {
  onFilter: (filters: { region: string; secteur: string }) => void;
}

const Filters: React.FC<FiltersProps> = ({ onFilter }) => {
  const [region, setRegion] = useState<string>("");
  const [secteur, setSecteur] = useState<string>("");
  const [regions, setRegions] = useState<string[]>([]);
  const [secteurs, setSecteurs] = useState<string[]>([]);

  useEffect(() => {
    // Charger les options de régions et de secteurs depuis le backend
    const fetchOptions = async () => {
      try {
        const [aoRes, bdcRes] = await Promise.all([
          fetch("/api/ao").then((res) => res.json()),
          fetch("/api/bdc").then((res) => res.json()),
        ]);

        const allRegions = Array.from(
          new Set([
            ...aoRes.map((ao: any) => ao.region).filter(Boolean),
            ...bdcRes.map((bdc: any) => bdc.lieu).filter(Boolean),
          ])
        );

        const allSecteurs = Array.from(
          new Set([
            ...aoRes.map((ao: any) => ao.secteur).filter(Boolean),
            ...bdcRes.map((bdc: any) => bdc.acheteur).filter(Boolean),
          ])
        );

        setRegions(allRegions);
        setSecteurs(allSecteurs);
      } catch (err) {
        console.error("Erreur de chargement des filtres:", err);
      }
    };

    fetchOptions();
  }, []);

  useEffect(() => {
    onFilter({ region, secteur });
  }, [region, secteur]);

  return (
    <div className="flex gap-4 mb-4">
      <select
        value={region}
        onChange={(e) => setRegion(e.target.value)}
        className="p-2 border rounded w-1/2"
      >
        <option value="">Toutes les régions</option>
        {regions.map((r) => (
          <option key={r} value={r}>
            {r}
          </option>
        ))}
      </select>

      <select
        value={secteur}
        onChange={(e) => setSecteur(e.target.value)}
        className="p-2 border rounded w-1/2"
      >
        <option value="">Tous les secteurs</option>
        {secteurs.map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Filters;
