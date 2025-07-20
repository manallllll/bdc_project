import React, { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 w-full mb-4">
      <input
        type="text"
        placeholder="Rechercher un BDC ou un AO..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-grow px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700"
      >
        Rechercher
      </button>
    </form>
  );
};

export default SearchBar;
