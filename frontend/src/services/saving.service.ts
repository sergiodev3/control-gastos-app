import api from '../lib/axios';
import type { Saving, SavingCreate } from '../types';

export const savingService = {
  async getAll(params?: { skip?: number; limit?: number }): Promise<Saving[]> {
    const response = await api.get<Saving[]>('/savings', { params });
    return response.data;
  },

  async getById(id: string): Promise<Saving> {
    const response = await api.get<Saving>(`/savings/${id}`);
    return response.data;
  },

  async create(data: SavingCreate): Promise<Saving> {
    const response = await api.post<Saving>('/savings', data);
    return response.data;
  },

  async update(id: string, data: Partial<SavingCreate>): Promise<Saving> {
    const response = await api.put<Saving>(`/savings/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/savings/${id}`);
  },
};
