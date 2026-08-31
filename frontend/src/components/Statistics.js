import React, { useEffect, useState } from 'react';
import { getStatistics } from '../services/taskApi';
import '../styles/Statistics.css';

function Statistics() {
  const [stats, setStats] = useState({
    total_tasks: 0,
    todo_count: 0,
    in_progress_count: 0,
    done_count: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    setLoading(true);
    setError(null);
    const result = await getStatistics();
    if (result.success) {
      setStats(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="statistics-container"><p>Loading statistics...</p></div>;
  }

  return (
    <div className="statistics-container">
      <h2>Task Statistics</h2>
      {error && <p className="error">{error}</p>}
      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-value">{stats.total_tasks}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        <div className="stat-card todo">
          <div className="stat-value">{stats.todo_count}</div>
          <div className="stat-label">TODO</div>
        </div>
        <div className="stat-card in-progress">
          <div className="stat-value">{stats.in_progress_count}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="stat-card done">
          <div className="stat-value">{stats.done_count}</div>
          <div className="stat-label">Done</div>
        </div>
      </div>
    </div>
  );
}

export default Statistics;
