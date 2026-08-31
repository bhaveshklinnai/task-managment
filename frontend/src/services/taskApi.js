import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Create a new task
 */
export const createTask = async (taskData) => {
  try {
    const response = await apiClient.post('/tasks', taskData);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to create task' };
  }
};

/**
 * Get all tasks with optional filters
 */
export const getTasks = async (search = null, status = null, priority = null) => {
  try {
    const params = {};
    if (search) params.search = search;
    if (status) params.status = status;
    if (priority) params.priority = priority;
    
    const response = await apiClient.get('/tasks', { params });
    return { success: true, data: response.data.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to fetch tasks' };
  }
};

/**
 * Get a single task by ID
 */
export const getTaskById = async (taskId) => {
  try {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to fetch task' };
  }
};

/**
 * Update a task
 */
export const updateTask = async (taskId, updateData) => {
  try {
    const response = await apiClient.put(`/tasks/${taskId}`, updateData);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to update task' };
  }
};

/**
 * Delete a task
 */
export const deleteTask = async (taskId) => {
  try {
    const response = await apiClient.delete(`/tasks/${taskId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to delete task' };
  }
};

/**
 * Get task statistics
 */
export const getStatistics = async () => {
  try {
    const response = await apiClient.get('/tasks/stats');
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: error.response?.data?.detail || 'Failed to fetch statistics' };
  }
};

export default apiClient;
