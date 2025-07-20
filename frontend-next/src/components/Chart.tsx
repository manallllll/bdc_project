// src/components/Chart.tsx
'use client';

import { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

interface BdcData {
  date_mise_en_ligne: string;
}

interface Props {
  data: BdcData[];
}

const Chart: React.FC<Props> = ({ data }) => {
  const [chartData, setChartData] = useState<{ date: string; count: number }[]>([]);

  useEffect(() => {
    const countByDate: { [key: string]: number } = {};
    data.forEach((bdc) => {
      const date = bdc.date_mise_en_ligne?.split(' ')[0]; // YYYY-MM-DD
      if (date) {
        countByDate[date] = (countByDate[date] || 0) + 1;
      }
    });

    const formatted = Object.entries(countByDate).map(([date, count]) => ({
      date,
      count,
    }));

    setChartData(formatted);
  }, [data]);

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-2">Évolution des BDC</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Chart;
