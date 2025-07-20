// src/components/DashboardCard.tsx
'use client';

import React from 'react';

export interface AoData {
  _id: string;
  url: string;
  titre: string;
  date_publication: string;
  description: string;
  fichier: string;
}

interface Props {
  data: AoData[];
}

const DashboardCard: React.FC<Props> = ({ data }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {data.map((ao) => (
        <div key={ao._id} className="bg-white rounded-2xl p-4 shadow-md border border-gray-200">
          <h3 className="text-lg font-semibold mb-2">{ao.titre}</h3>
          <p className="text-sm text-gray-600 mb-2">{ao.date_publication}</p>
          <p className="text-sm text-gray-700 mb-2 line-clamp-3">{ao.description}</p>
          <div className="flex justify-between mt-4 text-sm">
            <a href={ao.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Voir</a>
            <a href={ao.fichier} target="_blank" rel="noopener noreferrer" className="text-green-600 hover:underline">Télécharger</a>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DashboardCard;
