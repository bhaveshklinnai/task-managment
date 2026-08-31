import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

/**
 * Turn an axios failure into a single readable sentence.
 * FastAPI sends `detail` as a string for our own errors, but as an array of
 * field errors for request-body validation failures, so both are handled.
 */
const getErrorMessage = (error, fallback) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === 'string') {
    return detail;
  }
  if (Array.isArray(detail) && detail.length > 0) {
    return detail
      .map(item => {
        const field = item.loc?.[item.loc.length - 1];
        return field ? `${field}: ${item.msg}` : item.msg;
      })
      .join(', ');
  }
  if (error.response) {
    return `${fallback} (HTTP ${error.response.status})`;
  }
  return `${fallback}. Could not reach the API at ${API_URL}.`;
};

/** Create a new task. */
export const createTask = async (taskData) => {
  try {
    const response = await apiClient.post('/tasks', taskData);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to create task') };
  }
};

/** Get tasks, optionally searched by title and filtered by status/priority. */
export const getTasks = async ({ search, status, priority } = {}) => {
  try {
    const params = {};
    if (search) params.search = search;
    if (status) params.status = status;
    if (priority) params.priority = priority;

    const response = await apiClient.get('/tasks', { params });
    return { success: true, data: response.data.data };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to load tasks') };
  }
};

/** Get a single task by id. */
export const getTaskById = async (taskId) => {
  try {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to load task') };
  }
};

/** Update a task. */
export const updateTask = async (taskId, updateData) => {
  try {
    const response = await apiClient.put(`/tasks/${taskId}`, updateData);
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to update task') };
  }
};

/** Delete a task. */
export const deleteTask = async (taskId) => {
  try {
    await apiClient.delete(`/tasks/${taskId}`);
    return { success: true };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to delete task') };
  }
};

/** Get task statistics. */
export const getStatistics = async () => {
  try {
    const response = await apiClient.get('/tasks/stats');
    return { success: true, data: response.data };
  } catch (error) {
    return { success: false, error: getErrorMessage(error, 'Failed to load statistics') };
  }
};
