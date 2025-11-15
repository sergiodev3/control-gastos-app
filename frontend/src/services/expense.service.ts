import api from '../lib/axios';
import type { Expense, ExpenseCreate, ExpenseUpdate } from '../types';

export const expenseService = {
  async getAll(params?: { skip?: number; limit?: number }): Promise<Expense[]> {
    const response = await api.get<Expense[]>('/expenses', { params });
    return response.data;
  },

  async getById(id: string): Promise<Expense> {
    const response = await api.get<Expense>(`/expenses/${id}`);
    return response.data;
  },

  async create(data: ExpenseCreate): Promise<Expense> {
    const response = await api.post<Expense>('/expenses', data);
    return response.data;
  },

  async update(id: string, data: ExpenseUpdate): Promise<Expense> {
    const response = await api.put<Expense>(`/expenses/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/expenses/${id}`);
  },
};
