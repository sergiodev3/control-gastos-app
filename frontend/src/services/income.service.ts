import api from '../lib/axios';
import type { Income, IncomeCreate } from '../types';

export const incomeService = {
  async getAll(params?: { skip?: number; limit?: number }): Promise<Income[]> {
    const response = await api.get<Income[]>('/incomes', { params });
    return response.data;
  },

  async getById(id: string): Promise<Income> {
    const response = await api.get<Income>(`/incomes/${id}`);
    return response.data;
  },

  async create(data: IncomeCreate): Promise<Income> {
    const response = await api.post<Income>('/incomes', data);
    return response.data;
  },

  async update(id: string, data: Partial<IncomeCreate>): Promise<Income> {
    const response = await api.put<Income>(`/incomes/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/incomes/${id}`);
  },
};
