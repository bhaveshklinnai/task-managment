import React, { useState, useEffect } from 'react';
import Statistics from './Statistics';
import SearchFilter from './SearchFilter';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import { getTasks, createTask, updateTask, deleteTask } from '../services/taskApi';
import '../styles/Dashboard.css';

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [message, setMessage] = useState(null);
  const [currentFilters, setCurrentFilters] = useState({
    search: null,
    status: null,
    priority: null
  });

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    const result = await getTasks(
      currentFilters.search,
      currentFilters.status,
      currentFilters.priority
    );
    if (result.success) {
      setTasks(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleFilter = async (filters) => {
    setCurrentFilters(filters);
    setLoading(true);
    setError(null);
    const result = await getTasks(filters.search, filters.status, filters.priority);
    if (result.success) {
      setTasks(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleCreateTask = async (formData) => {
    const result = await createTask(formData);
    if (result.success) {
      setMessage('Task created successfully!');
      setShowForm(false);
      fetchTasks();
      setTimeout(() => setMessage(null), 3000);
    } else {
      setError(result.error);
    }
  };

  const handleUpdateTask = async (formData) => {
    const result = await updateTask(editingTask._id || editingTask.id, formData);
    if (result.success) {
      setMessage('Task updated successfully!');
      setEditingTask(null);
      setShowForm(false);
      fetchTasks();
      setTimeout(() => setMessage(null), 3000);
    } else {
      setError(result.error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    const result = await deleteTask(taskId);
    if (result.success) {
      setMessage('Task deleted successfully!');
      fetchTasks();
      setTimeout(() => setMessage(null), 3000);
    } else {
      setError(result.error);
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleFormSubmit = (formData) => {
    if (editingTask) {
      handleUpdateTask(formData);
    } else {
      handleCreateTask(formData);
    }
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Task Management Dashboard</h1>
        <button
          onClick={() => setShowForm(true)}
          className="btn btn-primary btn-lg"
        >
          + Create New Task
        </button>
      </div>

      {message && <div className="message success">{message}</div>}
      {error && <div className="message error">{error}</div>}

      {showForm && (
        <TaskForm
          task={editingTask}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseForm}
        />
      )}

      <Statistics />

      <SearchFilter onFilter={handleFilter} />

      <TaskList
        tasks={tasks}
        loading={loading}
        isEmpty={tasks.length === 0 && !loading && currentFilters.search === null && currentFilters.status === null && currentFilters.priority === null}
        onEdit={handleEditTask}
        onDelete={handleDeleteTask}
      />
    </div>
  );
}

export default Dashboard;
