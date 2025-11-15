// Tipos de autenticación
export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  full_name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Tipos de gastos
export type PaymentType = 
  | 'efectivo'
  | 'tarjeta_debito'
  | 'tarjeta_credito'
  | 'transferencia'
  | 'paypal'
  | 'otro';

export interface Expense {
  id: string;
  user_id: string;
  date: string;
  description: string;
  amount: number;
  payment_type: PaymentType;
  category?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ExpenseCreate {
  description: string;
  amount: number;
  payment_type: PaymentType;
  category?: string;
  notes?: string;
  date?: string;
}

export interface ExpenseUpdate {
  description?: string;
  amount?: number;
  payment_type?: PaymentType;
  category?: string;
  notes?: string;
  date?: string;
}

// Tipos de ingresos
export interface Income {
  id: string;
  user_id: string;
  date: string;
  description: string;
  amount: number;
  source?: string;
  is_recurring: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface IncomeCreate {
  description: string;
  amount: number;
  source?: string;
  is_recurring?: boolean;
  notes?: string;
  date?: string;
}

// Tipos de ahorros
export interface Saving {
  id: string;
  user_id: string;
  date: string;
  description: string;
  amount: number;
  goal_amount?: number;
  purpose?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface SavingCreate {
  description: string;
  amount: number;
  goal_amount?: number;
  purpose?: string;
  notes?: string;
  date?: string;
}

// Tipos de estadísticas
export interface Summary {
  total_expenses: number;
  total_incomes: number;
  total_savings: number;
  balance: number;
  period_start?: string;
  period_end?: string;
}

export interface MonthlyReport {
  year: number;
  month: number;
  total_expenses: number;
  total_incomes: number;
  total_savings: number;
  balance: number;
  expenses_by_category: Record<string, number>;
  expenses_by_payment_type: Record<string, number>;
}

// Tipos de paginación
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// Tipos de errores
export interface APIError {
  detail: string;
  timestamp?: string;
  path?: string;
}
