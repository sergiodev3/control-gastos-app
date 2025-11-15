import { ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Home, 
  TrendingDown, 
  TrendingUp, 
  PiggyBank, 
  BarChart3,
  User,
  LogOut
} from 'lucide-react';
import { useAuthStore } from '../store/auth.store';

interface MobileLayoutProps {
  children: ReactNode;
}

export default function MobileLayout({ children }: MobileLayoutProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();

  const navItems = [
    { icon: Home, label: 'Inicio', path: '/dashboard' },
    { icon: TrendingDown, label: 'Gastos', path: '/expenses' },
    { icon: TrendingUp, label: 'Ingresos', path: '/incomes' },
    { icon: PiggyBank, label: 'Ahorros', path: '/savings' },
    { icon: BarChart3, label: 'Stats', path: '/stats' },
  ];

  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="container-mobile py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Control de Gastos</h1>
              <p className="text-sm text-gray-600">Hola, {user?.full_name?.split(' ')[0] || 'Usuario'}</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => navigate('/profile')}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                aria-label="Perfil"
              >
                <User className="w-5 h-5 text-gray-600" />
              </button>
              <button
                onClick={handleLogout}
                className="p-2 rounded-lg hover:bg-red-50 transition-colors"
                aria-label="Cerrar sesión"
              >
                <LogOut className="w-5 h-5 text-red-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container-mobile py-6">
        {children}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
        <div className="grid grid-cols-5 gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`
                  flex flex-col items-center justify-center py-3 transition-colors
                  ${active 
                    ? 'text-primary-600' 
                    : 'text-gray-600 hover:text-gray-900'
                  }
                `}
                aria-label={item.label}
              >
                <Icon className={`w-6 h-6 ${active ? 'stroke-[2.5]' : 'stroke-2'}`} />
                <span className={`text-xs mt-1 font-medium ${active ? 'font-semibold' : ''}`}>
                  {item.label}
                </span>
              </button>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
