import React, { useState, useEffect } from 'react';
import { STATUS_OPTIONS, PRIORITY_OPTIONS } from '../constants';
import './TaskForm.css';

const BLANK_TASK = {
  title: '',
  description: '',
  status: 'TODO',
  priority: 'MEDIUM',
  assignee: ''
};

function TaskForm({ task, onSubmit, onCancel }) {
  const [formData, setFormData] = useState(BLANK_TASK);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    setFormData(
      task
        ? {
            title: task.title || '',
            description: task.description || '',
            status: task.status || 'TODO',
            priority: task.priority || 'MEDIUM',
            assignee: task.assignee || ''
          }
        : BLANK_TASK
    );
    setErrors({});
  }, [task]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 255) {
      newErrors.title = 'Title must be 255 characters or less';
    }
    if (!formData.assignee.trim()) {
      newErrors.assignee = 'Assignee is required';
    } else if (formData.assignee.length > 255) {
      newErrors.assignee = 'Assignee must be 255 characters or less';
    }
    if (formData.description.length > 2000) {
      newErrors.description = 'Description must be 2000 characters or less';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({
        ...formData,
        title: formData.title.trim(),
        description: formData.description.trim(),
        assignee: formData.assignee.trim()
      });
    }
  };

  return (
    <div className="task-form-container">
      <div className="task-form-content">
        <h2>{task ? 'Edit Task' : 'Create New Task'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter task title"
              className={errors.title ? 'form-input error' : 'form-input'}
            />
            {errors.title && <span className="error-message">{errors.title}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter task description"
              rows="4"
              maxLength={2000}
              className={errors.description ? 'form-input error' : 'form-input'}
            />
            {errors.description && (
              <span className="error-message">{errors.description}</span>
            )}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="form-input"
              >
                {STATUS_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <select
                id="priority"
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="form-input"
              >
                {PRIORITY_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="assignee">Assignee *</label>
            <input
              type="text"
              id="assignee"
              name="assignee"
              value={formData.assignee}
              onChange={handleChange}
              placeholder="Enter assignee name"
              className={errors.assignee ? 'form-input error' : 'form-input'}
            />
            {errors.assignee && <span className="error-message">{errors.assignee}</span>}
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              {task ? 'Update Task' : 'Create Task'}
            </button>
            <button type="button" onClick={onCancel} className="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TaskForm;
