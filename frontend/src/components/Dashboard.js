import React, { useCallback, useEffect, useState } from 'react';
import Statistics from './Statistics';
import SearchFilter from './SearchFilter';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import { getTasks, getStatistics, createTask, updateTask, deleteTask } from '../services/taskApi';
import './Dashboard.css';

const EMPTY_FILTERS = { search: '', status: '', priority: '' };

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const [filters, setFilters] = useState(EMPTY_FILTERS);
  // The search box updates on every keystroke; this holds the value actually
  // sent to the API, so typing does not fire a request per character.
  const [searchTerm, setSearchTerm] = useState('');
  // Bumped after create/update/delete to trigger a reload.
  const [reloadCount, setReloadCount] = useState(0);

  const { status, priority } = filters;
  const isFiltered = Boolean(searchTerm || status || priority);

  useEffect(() => {
    const timer = setTimeout(() => setSearchTerm(filters.search.trim()), 300);
    return () => clearTimeout(timer);
  }, [filters.search]);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      const [taskResult, statsResult] = await Promise.all([
        getTasks({ search: searchTerm, status, priority }),
        getStatistics()
      ]);

      // A slower earlier request must not overwrite newer results.
      if (cancelled) return;

      if (taskResult.success) {
        setTasks(taskResult.data);
        setError(null);
      } else {
        setTasks([]);
        setError(taskResult.error);
      }

      if (statsResult.success) {
        setStats(statsResult.data);
      }
      setLoading(false);
    };

    load();
    return () => {
      cancelled = true;
    };
  }, [searchTerm, status, priority, reloadCount]);

  const reload = useCallback(() => setReloadCount(count => count + 1), []);

  const showMessage = useCallback((text) => {
    setMessage(text);
    setTimeout(() => setMessage(null), 3000);
  }, []);

  const handleCreateTask = async (formData) => {
    const result = await createTask(formData);
    if (result.success) {
      setShowForm(false);
      showMessage('Task created successfully.');
      reload();
    } else {
      setError(result.error);
    }
  };

  const handleUpdateTask = async (formData) => {
    const result = await updateTask(editingTask.id, formData);
    if (result.success) {
      setEditingTask(null);
      setShowForm(false);
      showMessage('Task updated successfully.');
      reload();
    } else {
      setError(result.error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    const result = await deleteTask(taskId);
    if (result.success) {
      showMessage('Task deleted successfully.');
      reload();
    } else {
      setError(result.error);
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
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
          onClick={() => {
            setEditingTask(null);
            setShowForm(true);
          }}
          className="btn btn-primary btn-lg"
        >
          + Create New Task
        </button>
      </div>

      {message && <div className="message success">{message}</div>}
      {error && (
        <div className="message error">
          {error}
          <button onClick={() => setError(null)} className="message-dismiss">
            &times;
          </button>
        </div>
      )}

      {showForm && (
        <TaskForm
          task={editingTask}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onCancel={handleCloseForm}
        />
      )}

      <Statistics stats={stats} />

      <SearchFilter
        filters={filters}
        onChange={setFilters}
        onReset={() => setFilters(EMPTY_FILTERS)}
      />

      <TaskList
        tasks={tasks}
        loading={loading}
        isFiltered={isFiltered}
        onEdit={handleEditTask}
        onDelete={handleDeleteTask}
      />
    </div>
  );
}

export default Dashboard;
