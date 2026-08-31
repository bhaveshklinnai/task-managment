import React from 'react';
import TaskItem from './TaskItem';
import '../styles/TaskList.css';

function TaskList({ tasks, loading, onEdit, onDelete, isEmpty }) {
  if (loading) {
    return (
      <div className="task-list-container">
        <div className="loading">Loading tasks...</div>
      </div>
    );
  }

  if (isEmpty || tasks.length === 0) {
    return (
      <div className="task-list-container">
        <div className="empty-state">
          <p>No tasks found.</p>
          <p>Create one to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="task-list-container">
      <h2>Tasks ({tasks.length})</h2>
      <div className="task-list">
        {tasks.map(task => (
          <TaskItem
            key={task._id || task.id}
            task={task}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
}

export default TaskList;
