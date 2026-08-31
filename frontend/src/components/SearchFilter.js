import React, { useState } from 'react';
import '../styles/SearchFilter.css';

function SearchFilter({ onFilter }) {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');

  const handleFilter = () => {
    onFilter({
      search: search || null,
      status: status || null,
      priority: priority || null
    });
  };

  const handleReset = () => {
    setSearch('');
    setStatus('');
    setPriority('');
    onFilter({
      search: null,
      status: null,
      priority: null
    });
  };

  return (
    <div className="search-filter-container">
      <h3>Search & Filter</h3>
      <div className="filter-row">
        <input
          type="text"
          placeholder="Search by title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="filter-input"
        />
        
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="filter-select"
        >
          <option value="">All Statuses</option>
          <option value="TODO">TODO</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="DONE">Done</option>
        </select>

        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="filter-select"
        >
          <option value="">All Priorities</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
        </select>

        <button onClick={handleFilter} className="btn btn-primary">
          Filter
        </button>
        <button onClick={handleReset} className="btn btn-secondary">
          Reset
        </button>
      </div>
    </div>
  );
}

export default SearchFilter;
