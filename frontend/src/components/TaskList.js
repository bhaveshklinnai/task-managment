import React from 'react';
import TaskItem from './TaskItem';
import './TaskList.css';

function TaskList({ tasks, loading, isFiltered, onEdit, onDelete }) {
  if (loading) {
    return (
      <div className="task-list-container">
        <div className="loading">Loading tasks...</div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="task-list-container">
        <div className="empty-state">
          {isFiltered ? (
            <>
              <p>No tasks match your search and filters.</p>
              <p>Try a different title or reset the filters.</p>
            </>
          ) : (
            <>
              <p>No tasks yet.</p>
              <p>Create one to get started.</p>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="task-list-container">
      <h2>Tasks ({tasks.length})</h2>
      <div className="task-list">
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} onEdit={onEdit} onDelete={onDelete} />
        ))}
      </div>
    </div>
  );
}

export default TaskList;
