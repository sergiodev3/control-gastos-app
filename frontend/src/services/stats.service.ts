import api from '../lib/axios';
import type { Summary, MonthlyReport } from '../types';

export const statsService = {
  async getSummary(): Promise<Summary> {
    const response = await api.get<Summary>('/stats/summary');
    return response.data;
  },

  async getMonthlyReport(year: number, month: number): Promise<MonthlyReport> {
    const response = await api.get<MonthlyReport>(`/stats/monthly/${year}/${month}`);
    return response.data;
  },
};
