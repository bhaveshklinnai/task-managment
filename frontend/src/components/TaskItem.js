import React from 'react';
import '../styles/TaskItem.css';

function TaskItem({ task, onEdit, onDelete }) {
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const getPriorityClass = (priority) => {
    return `priority-${priority.toLowerCase()}`;
  };

  const getStatusClass = (status) => {
    return `status-${status.toLowerCase().replace('_', '-')}`;
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      onDelete(task._id || task.id);
    }
  };

  return (
    <div className="task-item">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <div className="task-badges">
          <span className={`badge status ${getStatusClass(task.status)}`}>
            {task.status.replace('_', ' ')}
          </span>
          <span className={`badge priority ${getPriorityClass(task.priority)}`}>
            {task.priority}
          </span>
        </div>
      </div>
      
      <p className="task-description">{task.description}</p>
      
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
