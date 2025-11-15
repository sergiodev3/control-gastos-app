import { create } from 'zustand';
import type { User, LoginCredentials, RegisterData } from '../types';
import { authService } from '../services/auth.service';
import toast from 'react-hot-toast';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: authService.getUser(),
  token: authService.getToken(),
  isLoading: false,
  isAuthenticated: !!authService.getToken(),

  login: async (credentials) => {
    try {
      set({ isLoading: true });
      const { access_token } = await authService.login(credentials);
      
      authService.setToken(access_token);
      
      // Obtener datos del usuario
      const user = await authService.getProfile();
      authService.setUser(user);
      
      set({
        user,
        token: access_token,
        isAuthenticated: true,
        isLoading: false,
      });
      
      toast.success('¡Bienvenido de nuevo!');
    } catch (error: any) {
      set({ isLoading: false });
      const message = error.response?.data?.detail || 'Error al iniciar sesión';
      toast.error(message);
      throw error;
    }
  },

  register: async (data) => {
    try {
      set({ isLoading: true });
      await authService.register(data);
      
      // Auto-login después del registro
      await useAuthStore.getState().login({
        email: data.email,
        password: data.password,
      });
      
      toast.success('¡Cuenta creada exitosamente!');
    } catch (error: any) {
      set({ isLoading: false });
      const message = error.response?.data?.detail || 'Error al crear cuenta';
      toast.error(message);
      throw error;
    }
  },

  logout: () => {
    authService.logout();
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
    toast.success('Sesión cerrada');
  },

  loadUser: async () => {
    try {
      const token = authService.getToken();
      if (!token) {
        set({ isAuthenticated: false });
        return;
      }

      set({ isLoading: true });
      const user = await authService.getProfile();
      authService.setUser(user);
      
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      authService.logout();
      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },

  setUser: (user) => {
    set({ user });
    authService.setUser(user);
  },
}));
