import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingDown, TrendingUp, PiggyBank, Wallet, RefreshCw } from 'lucide-react';
import MobileLayout from '../components/MobileLayout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { statsService } from '../services/stats.service';
import type { Summary } from '../types';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<Summary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      setIsLoading(true);
      const data = await statsService.getSummary();
      console.log('Summary data:', data); // Debug
      setSummary(data);
    } catch (error) {
      console.error('Error loading summary:', error);
      toast.error('Error al cargar el resumen');
    } finally {
      setIsLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
    }).format(amount);
  };

  return (
    <MobileLayout>
      <div className="space-y-6">
        {/* Balance principal */}
        <Card className="bg-linear-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-blue-700 text-sm font-medium">Balance Total</span>
            <Wallet className="w-5 h-5 text-blue-600" />
          </div>
          <h2 className="text-3xl font-bold mb-1 text-gray-900">
            {isLoading ? '...' : formatCurrency(summary?.balance || 0)}
          </h2>
          <p className="text-blue-700 text-sm">
            {summary && summary.balance >= 0 ? 'Tienes un balance positivo' : 'Balance negativo'}
          </p>
        </Card>

        {/* Resumen de finanzas */}
        <div className="grid grid-cols-1 gap-4">
          <Card className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Gastos</p>
              <p className="text-2xl font-bold text-red-600">
                {isLoading ? '...' : formatCurrency(summary?.total_expenses || 0)}
              </p>
            </div>
            <div className="p-3 bg-red-50 rounded-lg">
              <TrendingDown className="w-6 h-6 text-red-600" />
            </div>
          </Card>

          <Card className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Ingresos</p>
              <p className="text-2xl font-bold text-green-600">
                {isLoading ? '...' : formatCurrency(summary?.total_incomes || 0)}
              </p>
            </div>
            <div className="p-3 bg-green-50 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </Card>

          <Card className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Ahorros</p>
              <p className="text-2xl font-bold text-blue-600">
                {isLoading ? '...' : formatCurrency(summary?.total_savings || 0)}
              </p>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg">
              <PiggyBank className="w-6 h-6 text-blue-600" />
            </div>
          </Card>
        </div>

        {/* Acciones rápidas */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Acciones Rápidas</h3>
            <Button
              size="sm"
              variant="secondary"
              onClick={loadSummary}
              isLoading={isLoading}
            >
              <RefreshCw className="w-4 h-4" />
            </Button>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <button 
              onClick={() => navigate('/expenses')} 
              className="btn btn-primary flex flex-col items-center py-4"
            >
              <TrendingDown className="w-6 h-6 mb-1" />
              <span className="text-xs">Gasto</span>
            </button>
            <button 
              onClick={() => navigate('/incomes')} 
              className="btn bg-green-600 text-white hover:bg-green-700 flex flex-col items-center py-4"
            >
              <TrendingUp className="w-6 h-6 mb-1" />
              <span className="text-xs">Ingreso</span>
            </button>
            <button 
              onClick={() => navigate('/savings')} 
              className="btn bg-blue-600 text-white hover:bg-blue-700 flex flex-col items-center py-4"
            >
              <PiggyBank className="w-6 h-6 mb-1" />
              <span className="text-xs">Ahorro</span>
            </button>
          </div>
        </div>
      </div>
    </MobileLayout>
  );
}
