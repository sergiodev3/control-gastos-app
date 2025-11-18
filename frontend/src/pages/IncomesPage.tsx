import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { Plus, TrendingUp, Search, Trash2, Edit2, Calendar, RefreshCw } from 'lucide-react';
import MobileLayout from '../components/MobileLayout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Textarea from '../components/ui/Textarea';
import Modal from '../components/ui/Modal';
import { incomeService } from '../services/income.service';
import type { Income, IncomeCreate } from '../types';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

const INCOME_SOURCES = [
  'Salario',
  'Freelance',
  'Negocio Propio',
  'Inversiones',
  'Rentas',
  'Bonos',
  'Comisiones',
  'Regalos',
  'Ventas',
  'Otros',
];

export default function IncomesPage() {
  const [incomes, setIncomes] = useState<Income[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingIncome, setEditingIncome] = useState<Income | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState<IncomeCreate>({
    description: '',
    amount: 0,
    source: '',
    is_recurring: false,
    notes: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadIncomes();
  }, []);

  const loadIncomes = async () => {
    try {
      setIsLoading(true);
      const data = await incomeService.getAll();
      setIncomes(data.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
    } catch {
      toast.error('Error al cargar ingresos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenModal = (income?: Income) => {
    if (income) {
      setEditingIncome(income);
      setFormData({
        description: income.description,
        amount: income.amount,
        source: income.source || '',
        is_recurring: income.is_recurring,
        notes: income.notes || '',
        date: income.date.split('T')[0],
      });
    } else {
      setEditingIncome(null);
      setFormData({
        description: '',
        amount: 0,
        source: '',
        is_recurring: false,
        notes: '',
        date: new Date().toISOString().split('T')[0],
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingIncome(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    if (formData.amount <= 0) {
      toast.error('El monto debe ser mayor a 0');
      return;
    }

    try {
      setIsSubmitting(true);
      
      if (editingIncome) {
        await incomeService.update(editingIncome.id, formData);
        toast.success('Ingreso actualizado exitosamente');
      } else {
        await incomeService.create(formData);
        toast.success('Ingreso registrado exitosamente');
      }
      
      await loadIncomes();
      handleCloseModal();
    } catch (error: unknown) {
      const message = error instanceof Error && 'response' in error 
        ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Error al guardar el ingreso'
        : 'Error al guardar el ingreso';
      toast.error(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Estás seguro de eliminar este ingreso?')) return;

    try {
      await incomeService.delete(id);
      toast.success('Ingreso eliminado exitosamente');
      await loadIncomes();
    } catch {
      toast.error('Error al eliminar el ingreso');
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
    }).format(amount);
  };

  // Filtrar ingresos
  const filteredIncomes = incomes.filter(income => {
    const matchesSearch = income.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         income.source?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         income.notes?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  const totalIncomes = filteredIncomes.reduce((sum, inc) => sum + inc.amount, 0);

  return (
    <MobileLayout>
      <div className="space-y-4">
        {/* Header con total */}
        <Card className="bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-green-100 text-sm font-medium">Total de Ingresos</span>
            <TrendingUp className="w-5 h-5 text-green-200" />
          </div>
          <h2 className="text-3xl font-bold">
            {formatCurrency(totalIncomes)}
          </h2>
          <p className="text-green-100 text-sm mt-1">
            {filteredIncomes.length} {filteredIncomes.length === 1 ? 'ingreso' : 'ingresos'}
          </p>
        </Card>

        {/* Búsqueda */}
        <div className="space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Buscar ingresos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          <Button onClick={() => handleOpenModal()} fullWidth>
            <Plus className="w-5 h-5" />
            Agregar Ingreso
          </Button>
        </div>

        {/* Lista de ingresos */}
        <div className="space-y-3">
          {isLoading ? (
            <Card>
              <p className="text-center text-gray-500">Cargando ingresos...</p>
            </Card>
          ) : filteredIncomes.length === 0 ? (
            <Card>
              <div className="text-center py-8">
                <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-2">No hay ingresos registrados</p>
                <p className="text-sm text-gray-400">
                  {searchTerm ? 'Intenta con otros términos de búsqueda' : 'Comienza agregando tu primer ingreso'}
                </p>
              </div>
            </Card>
          ) : (
            filteredIncomes.map((income) => (
              <Card key={income.id} className="hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">💰</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold text-gray-900 truncate">
                            {income.description}
                          </h3>
                          {income.is_recurring && (
                            <span className="flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 rounded-full">
                              <RefreshCw className="w-3 h-3" />
                              Recurrente
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Calendar className="w-3 h-3" />
                          <span>
                            {format(new Date(income.date), "d 'de' MMMM, yyyy", { locale: es })}
                          </span>
                        </div>
                      </div>
                    </div>

                    {income.source && (
                      <span className="inline-block px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full mt-1">
                        {income.source}
                      </span>
                    )}

                    {income.notes && (
                      <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                        {income.notes}
                      </p>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    <span className="text-lg font-bold text-green-600">
                      +{formatCurrency(income.amount)}
                    </span>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleOpenModal(income)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                        aria-label="Editar"
                      >
                        <Edit2 className="w-4 h-4 text-gray-600" />
                      </button>
                      <button
                        onClick={() => handleDelete(income.id)}
                        className="p-2 rounded-lg hover:bg-red-50 transition-colors"
                        aria-label="Eliminar"
                      >
                        <Trash2 className="w-4 h-4 text-red-600" />
                      </button>
                    </div>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>

      {/* Modal de formulario */}
      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingIncome ? 'Editar Ingreso' : 'Nuevo Ingreso'}
        size="md"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Descripción"
            type="text"
            placeholder="Ej: Pago de salario"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            required
          />

          <Input
            label="Monto"
            type="number"
            step="0.01"
            min="0.01"
            placeholder="0.00"
            value={formData.amount || ''}
            onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
            required
          />

          <Select
            label="Fuente de Ingreso"
            value={formData.source}
            onChange={(e) => setFormData({ ...formData, source: e.target.value })}
            options={INCOME_SOURCES.map(source => ({ value: source, label: source }))}
          />

          <Input
            label="Fecha"
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_recurring"
              checked={formData.is_recurring}
              onChange={(e) => setFormData({ ...formData, is_recurring: e.target.checked })}
              className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <label htmlFor="is_recurring" className="text-sm font-medium text-gray-700">
              Ingreso recurrente (mensual)
            </label>
          </div>

          <Textarea
            label="Notas (opcional)"
            placeholder="Agrega notas adicionales..."
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          />

          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={handleCloseModal}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              fullWidth
              isLoading={isSubmitting}
              variant="success"
            >
              {editingIncome ? 'Actualizar' : 'Guardar'}
            </Button>
          </div>
        </form>
      </Modal>
    </MobileLayout>
  );
}
