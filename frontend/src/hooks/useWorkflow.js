import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '../services/apiConfig';

// --- Upload Document ---
export const useUploadDocument = () => {
  return useMutation({
    mutationFn: async (file) => {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return data;
    },
    retry: false, // Never auto-retry uploads
  });
};

// --- Run Workflow ---
export const useRunWorkflow = () => {
  return useMutation({
    mutationFn: async (payload) => {
      const { data } = await api.post('/workflow/run', payload);
      return data;
    },
    retry: false,
  });
};

// --- Get Dashboard ---
export const useDashboard = (authorizationId) => {
  return useQuery({
    queryKey: ['dashboard', authorizationId],
    queryFn: async () => {
      const { data } = await api.get(`/workflow/dashboard/${authorizationId}`);
      return data;
    },
    enabled: !!authorizationId,
    staleTime: Infinity,    // Immutable once processed
    gcTime: 1000 * 60 * 30, // 30 min cache
    retry: 3,
  });
};
