import React from 'react';
import './Statistics.css';

/**
 * Task counts. The numbers come from the API (calculated in MongoDB) and are
 * reloaded by Dashboard after every change, so they always match the database.
 */
function Statistics({ stats }) {
  if (!stats) {
    return (
      <div className="statistics-container">
        <p className="stats-loading">Loading statistics...</p>
      </div>
    );
  }

  const cards = [
    { key: 'total', label: 'Total Tasks', value: stats.total_tasks },
    { key: 'todo', label: 'TODO', value: stats.todo_count },
    { key: 'in-progress', label: 'In Progress', value: stats.in_progress_count },
    { key: 'done', label: 'Done', value: stats.done_count }
  ];

  return (
    <div className="statistics-container">
      <h2>Task Statistics</h2>
      <div className="stats-grid">
        {cards.map(card => (
          <div key={card.key} className={`stat-card ${card.key}`}>
            <div className="stat-value">{card.value}</div>
            <div className="stat-label">{card.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Statistics;
