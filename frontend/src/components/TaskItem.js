import React from 'react';
import './TaskItem.css';

/**
 * The API sends dates as UTC ISO-8601 strings (e.g. 2026-08-31T11:45:14+00:00),
 * so the browser converts them to the viewer's local time correctly.
 */
const formatDate = (value) => {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

function TaskItem({ task, onEdit, onDelete }) {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      onDelete(task.id);
    }
  };

  return (
    <div className="task-item">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <div className="task-badges">
          <span className={`badge status status-${task.status.toLowerCase().replace('_', '-')}`}>
            {task.status.replace('_', ' ')}
          </span>
          <span className={`badge priority priority-${task.priority.toLowerCase()}`}>
            {task.priority}
          </span>
        </div>
      </div>

      {task.description && <p className="task-description">{task.description}</p>}

      <div className="task-meta">
        <div className="meta-item">
          <span className="meta-label">Assignee:</span>
          <span className="meta-value">{task.assignee}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Created:</span>
          <span className="meta-value">{formatDate(task.created_date)}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Updated:</span>
          <span className="meta-value">{formatDate(task.updated_date)}</span>
        </div>
      </div>

      <div className="task-actions">
        <button onClick={() => onEdit(task)} className="btn btn-sm btn-primary">
          Edit
        </button>
        <button onClick={handleDelete} className="btn btn-sm btn-danger">
          Delete
        </button>
      </div>
    </div>
  );
}

export default TaskItem;
