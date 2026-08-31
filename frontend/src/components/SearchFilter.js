import React from 'react';
import { STATUS_OPTIONS, PRIORITY_OPTIONS } from '../constants';
import './SearchFilter.css';

/**
 * Search and filter controls. The values live in Dashboard, which reloads the
 * task list whenever they change, so results update as you type or select.
 */
function SearchFilter({ filters, onChange, onReset }) {
  const handleChange = (event) => {
    const { name, value } = event.target;
    onChange({ ...filters, [name]: value });
  };

  const hasFilters = Boolean(filters.search || filters.status || filters.priority);

  return (
    <div className="search-filter-container">
      <h3>Search &amp; Filter</h3>
      <div className="filter-row">
        <input
          type="text"
          name="search"
          placeholder="Search by title..."
          value={filters.search}
          onChange={handleChange}
          className="filter-input"
          aria-label="Search tasks by title"
        />

        <select
          name="status"
          value={filters.status}
          onChange={handleChange}
          className="filter-select"
          aria-label="Filter by status"
        >
          <option value="">All Statuses</option>
          {STATUS_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        <select
          name="priority"
          value={filters.priority}
          onChange={handleChange}
          className="filter-select"
          aria-label="Filter by priority"
        >
          <option value="">All Priorities</option>
          {PRIORITY_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>

        <button onClick={onReset} className="btn btn-secondary" disabled={!hasFilters}>
          Reset
        </button>
      </div>
    </div>
  );
}

export default SearchFilter;
