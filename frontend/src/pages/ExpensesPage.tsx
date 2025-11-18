import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { Plus, TrendingDown, Search, Filter, Trash2, Edit2, Calendar } from 'lucide-react';
import MobileLayout from '../components/MobileLayout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Textarea from '../components/ui/Textarea';
import Modal from '../components/ui/Modal';
import { expenseService } from '../services/expense.service';
import type { Expense, ExpenseCreate, PaymentType } from '../types';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

const PAYMENT_TYPES = [
  { value: 'efectivo', label: '💵 Efectivo' },
  { value: 'tarjeta_debito', label: '💳 Tarjeta de Débito' },
  { value: 'tarjeta_credito', label: '💳 Tarjeta de Crédito' },
  { value: 'transferencia', label: '🏦 Transferencia' },
  { value: 'paypal', label: '💰 PayPal' },
  { value: 'otro', label: '📝 Otro' },
];

const CATEGORIES = [
  'Alimentación',
  'Transporte',
  'Vivienda',
  'Servicios',
  'Entretenimiento',
  'Salud',
  'Educación',
  'Compras',
  'Otros',
];

export default function ExpensesPage() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');

  const [formData, setFormData] = useState<ExpenseCreate>({
    description: '',
    amount: 0,
    payment_type: 'efectivo' as PaymentType,
    category: '',
    notes: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadExpenses();
  }, []);

  const loadExpenses = async () => {
    try {
      setIsLoading(true);
      const data = await expenseService.getAll();
      setExpenses(data.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
    } catch (error) {
      toast.error('Error al cargar gastos');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenModal = (expense?: Expense) => {
    if (expense) {
      setEditingExpense(expense);
      setFormData({
        description: expense.description,
        amount: expense.amount,
        payment_type: expense.payment_type,
        category: expense.category || '',
        notes: expense.notes || '',
        date: expense.date.split('T')[0],
      });
    } else {
      setEditingExpense(null);
      setFormData({
        description: '',
        amount: 0,
        payment_type: 'efectivo' as PaymentType,
        category: '',
        notes: '',
        date: new Date().toISOString().split('T')[0],
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingExpense(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    if (formData.amount <= 0) {
      toast.error('El monto debe ser mayor a 0');
      return;
    }

    try {
      setIsSubmitting(true);
      
      if (editingExpense) {
        await expenseService.update(editingExpense.id, formData);
        toast.success('Gasto actualizado exitosamente');
      } else {
        await expenseService.create(formData);
        toast.success('Gasto registrado exitosamente');
      }
      
      await loadExpenses();
      handleCloseModal();
    } catch (error: unknown) {
      const message = error instanceof Error && 'response' in error 
        ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Error al guardar el gasto'
        : 'Error al guardar el gasto';
      toast.error(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('¿Estás seguro de eliminar este gasto?')) return;

    try {
      await expenseService.delete(id);
      toast.success('Gasto eliminado exitosamente');
      await loadExpenses();
    } catch {
      toast.error('Error al eliminar el gasto');
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
    }).format(amount);
  };

  const getPaymentTypeIcon = (type: PaymentType) => {
    const typeObj = PAYMENT_TYPES.find(pt => pt.value === type);
    return typeObj?.label.split(' ')[0] || '💳';
  };

  // Filtrar gastos
  const filteredExpenses = expenses.filter(expense => {
    const matchesSearch = expense.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         expense.notes?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !filterCategory || expense.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const totalExpenses = filteredExpenses.reduce((sum, exp) => sum + exp.amount, 0);

  return (
    <MobileLayout>
      <div className="space-y-4">
        {/* Header con total */}
        <Card className="bg-gradient-to-br from-red-500 to-red-600 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-red-100 text-sm font-medium">Total de Gastos</span>
            <TrendingDown className="w-5 h-5 text-red-200" />
          </div>
          <h2 className="text-3xl font-bold">
            {formatCurrency(totalExpenses)}
          </h2>
          <p className="text-red-100 text-sm mt-1">
            {filteredExpenses.length} {filteredExpenses.length === 1 ? 'gasto' : 'gastos'}
          </p>
        </Card>

        {/* Búsqueda y filtros */}
        <div className="space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Buscar gastos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          <div className="flex gap-2">
            <div className="flex-1">
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                <Select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  options={CATEGORIES.map(cat => ({ value: cat, label: cat }))}
                  className="pl-10"
                />
              </div>
            </div>
            <Button onClick={() => handleOpenModal()}>
              <Plus className="w-5 h-5" />
              Agregar
            </Button>
          </div>
        </div>

        {/* Lista de gastos */}
        <div className="space-y-3">
          {isLoading ? (
            <Card>
              <p className="text-center text-gray-500">Cargando gastos...</p>
            </Card>
          ) : filteredExpenses.length === 0 ? (
            <Card>
              <div className="text-center py-8">
                <TrendingDown className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-2">No hay gastos registrados</p>
                <p className="text-sm text-gray-400">
                  {searchTerm || filterCategory ? 'Intenta con otros filtros' : 'Comienza agregando tu primer gasto'}
                </p>
              </div>
            </Card>
          ) : (
            filteredExpenses.map((expense) => (
              <Card key={expense.id} className="hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">{getPaymentTypeIcon(expense.payment_type)}</span>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 truncate">
                          {expense.description}
                        </h3>
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Calendar className="w-3 h-3" />
                          <span>
                            {format(new Date(expense.date), "d 'de' MMMM, yyyy", { locale: es })}
                          </span>
                        </div>
                      </div>
                    </div>

                    {expense.category && (
                      <span className="inline-block px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full mt-1">
                        {expense.category}
                      </span>
                    )}

                    {expense.notes && (
                      <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                        {expense.notes}
                      </p>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    <span className="text-lg font-bold text-red-600">
                      -{formatCurrency(expense.amount)}
                    </span>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleOpenModal(expense)}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                        aria-label="Editar"
                      >
                        <Edit2 className="w-4 h-4 text-gray-600" />
                      </button>
                      <button
                        onClick={() => handleDelete(expense.id)}
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
        title={editingExpense ? 'Editar Gasto' : 'Nuevo Gasto'}
        size="md"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Descripción"
            type="text"
            placeholder="Ej: Compra de supermercado"
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
            label="Tipo de Pago"
            value={formData.payment_type}
            onChange={(e) => setFormData({ ...formData, payment_type: e.target.value as PaymentType })}
            options={PAYMENT_TYPES}
            required
          />

          <Select
            label="Categoría"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            options={CATEGORIES.map(cat => ({ value: cat, label: cat }))}
          />

          <Input
            label="Fecha"
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />

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
            >
              {editingExpense ? 'Actualizar' : 'Guardar'}
            </Button>
          </div>
        </form>
      </Modal>
    </MobileLayout>
  );
}
