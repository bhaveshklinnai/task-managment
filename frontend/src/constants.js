/**
 * The allowed status and priority values, defined once.
 *
 * These mirror VALID_STATUSES and VALID_PRIORITIES in
 * backend/app/utils/validation.py, which is what actually enforces them. The
 * `value` is what the API expects; the `label` is what the user reads.
 */

export const STATUS_OPTIONS = [
  { value: 'TODO', label: 'TODO' },
  { value: 'IN_PROGRESS', label: 'In Progress' },
  { value: 'DONE', label: 'Done' }
];

export const PRIORITY_OPTIONS = [
  { value: 'LOW', label: 'Low' },
  { value: 'MEDIUM', label: 'Medium' },
  { value: 'HIGH', label: 'High' }
];
