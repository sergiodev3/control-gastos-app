import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import { Plus, PiggyBank, Target, TrendingUp, Trash2, Edit2, Calendar } from 'lucide-react';
import MobileLayout from '../components/MobileLayout';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import CurrencyInput from '../components/ui/CurrencyInput';
import Textarea from '../components/ui/Textarea';
import Modal from '../components/ui/Modal';
import { savingService } from '../services/saving.service';
import type { Saving, SavingCreate } from '../types';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export default function SavingsPage() {
  const [savings, setSavings] = useState<Saving[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingSaving, setEditingSaving] = useState<Saving | null>(null);
  const [viewMode, setViewMode] = useState<'goals' | 'list'>('goals');

  const [formData, setFormData] = useState<SavingCreate>({
    amount: 0,
    transaction_type: 'deposito',
    purpose: '',
    goal_amount: undefined,
    notes: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadSavings();
  }, []);

  const loadSavings = async () => {
    try {
      setIsLoading(true);
      const data = await savingService.getAll();
      setSavings(data.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
    } catch (error) {
      toast.error('Error al cargar ahorros');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenModal = (saving?: Saving) => {
    if (saving) {
      setEditingSaving(saving);
      setFormData({
        amount: saving.amount,
        transaction_type: saving.transaction_type,
        purpose: saving.purpose || '',
        goal_amount: saving.goal_amount,
        notes: saving.notes || '',
        date: saving.date.split('T')[0],
      });
    } else {
      setEditingSaving(null);
      setFormData({
        amount: 0,
        transaction_type: 'deposito',
        purpose: '',
        goal_amount: undefined,
        notes: '',
        date: new Date().toISOString().split('T')[0],
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingSaving(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (formData.amount <= 0) {
      toast.error('El monto debe ser mayor a 0');
      return;
    }

    try {
      setIsSubmitting(true);

      if (editingSaving) {
        await savingService.update(editingSaving.id, formData);
        toast.success('Ahorro actualizado exitosamente');
      } else {
        await savingService.create(formData);
        toast.success('Ahorro registrado exitosamente');
      }

      handleCloseModal();
      await loadSavings();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Error al guardar el ahorro';
      toast.error(message, { duration: 8000 });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('¿Estás seguro de eliminar este ahorro?')) return;

    try {
      await savingService.delete(id);
      toast.success('Ahorro eliminado exitosamente');
      await loadSavings();
    } catch {
      toast.error('Error al eliminar el ahorro');
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
    }).format(amount);
  };

  // Agrupar ahorros por meta (purpose)
  const groupedSavings = savings.reduce((acc, saving) => {
    const purpose = saving.purpose || 'Sin propósito';
    if (!acc[purpose]) {
      acc[purpose] = [];
    }
    acc[purpose].push(saving);
    return acc;
  }, {} as Record<string, Saving[]>);

  // Calcular totales por meta
  const goals = Object.entries(groupedSavings).map(([purpose, savingsList]) => {
    // Calcular total considerando depósitos y retiros
    const totalSaved = savingsList.reduce((sum, s) => {
      return sum + (s.transaction_type === 'deposito' ? s.amount : -s.amount);
    }, 0);
    const goalAmount = savingsList.find(s => s.goal_amount)?.goal_amount || 0;
    const progress = goalAmount > 0 ? (totalSaved / goalAmount) * 100 : 0;
    const lastUpdate = savingsList[0].date;
    
    return {
      purpose,
      totalSaved,
      goalAmount,
      progress: Math.min(progress, 100),
      savingsList,
      lastUpdate,
    };
  });

  // Calcular total de ahorros neto (depósitos - retiros)
  const totalSavings = savings.reduce((sum, s) => {
    return sum + (s.transaction_type === 'deposito' ? s.amount : -s.amount);
  }, 0);

  return (
    <MobileLayout>
      <div className="space-y-4">
        {/* Header con total */}
        <Card className="bg-linear-to-br from-blue-500 to-blue-600 text-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-blue-100 text-sm font-medium">Total Ahorrado</span>
            <PiggyBank className="w-5 h-5 text-blue-200" />
          </div>
          <h2 className="text-3xl font-bold">
            {formatCurrency(totalSavings)}
          </h2>
          <p className="text-blue-100 text-sm mt-1">
            {goals.length} {goals.length === 1 ? 'meta' : 'metas'} activas
          </p>
        </Card>

        {/* Toggle de vista */}
        <div className="flex gap-2">
          <Button
            variant={viewMode === 'goals' ? 'primary' : 'secondary'}
            onClick={() => setViewMode('goals')}
            className="flex-1"
          >
            <Target className="w-4 h-4 mr-2" />
            Por Metas
          </Button>
          <Button
            variant={viewMode === 'list' ? 'primary' : 'secondary'}
            onClick={() => setViewMode('list')}
            className="flex-1"
          >
            <Calendar className="w-4 h-4 mr-2" />
            Lista
          </Button>
        </div>

        {/* Botón agregar */}
        <Button onClick={() => handleOpenModal()} fullWidth>
          <Plus className="w-5 h-5 mr-2" />
          Registrar Ahorro
        </Button>

        {/* Vista por metas */}
        {viewMode === 'goals' && (
          <div className="space-y-3">
            {isLoading ? (
              <Card>
                <p className="text-center text-gray-500">Cargando metas...</p>
              </Card>
            ) : goals.length === 0 ? (
              <Card>
                <div className="text-center py-8">
                  <Target className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">No hay metas de ahorro</p>
                  <p className="text-sm text-gray-400">
                    Comienza registrando tu primer ahorro con una meta
                  </p>
                </div>
              </Card>
            ) : (
              goals.map((goal) => (
                <Card key={goal.purpose} className="hover:shadow-md transition-shadow">
                  <div className="space-y-3">
                    {/* Header de la meta */}
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <Target className="w-5 h-5 text-blue-600" />
                          <h3 className="font-semibold text-gray-900">{goal.purpose}</h3>
                        </div>
                        <p className="text-sm text-gray-500">
                          {format(new Date(goal.lastUpdate), "d 'de' MMMM, yyyy", { locale: es })}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">Ahorrado</p>
                        <p className="font-bold text-blue-600">{formatCurrency(goal.totalSaved)}</p>
                      </div>
                    </div>

                    {/* Barra de progreso */}
                    {goal.goalAmount > 0 && (
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm text-gray-600">
                            Meta: {formatCurrency(goal.goalAmount)}
                          </span>
                          <span className="text-sm font-semibold text-blue-600">
                            {goal.progress.toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-linear-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-500 flex items-center justify-end pr-1"
                            style={{ width: `${goal.progress}%` }}
                          >
                            {goal.progress > 10 && (
                              <TrendingUp className="w-3 h-3 text-white" />
                            )}
                          </div>
                        </div>
                        {goal.progress >= 100 && (
                          <p className="text-sm text-green-600 font-medium mt-2">
                            🎉 ¡Meta alcanzada!
                          </p>
                        )}
                      </div>
                    )}

                    {/* Lista de movimientos de esta meta */}
                    <div className="border-t pt-3 mt-3">
                      <p className="text-xs text-gray-500 mb-2">
                        {goal.savingsList.length} {goal.savingsList.length === 1 ? 'movimiento' : 'movimientos'}
                      </p>
                      <div className="space-y-2">
                        {goal.savingsList.slice(0, 3).map((saving) => (
                          <div
                            key={saving.id}
                            className="flex items-center justify-between text-sm"
                          >
                            <div className="flex items-center gap-2">
                              <span className="text-gray-600">
                                {format(new Date(saving.date), 'd MMM yyyy', { locale: es })}
                              </span>
                              {saving.transaction_type === 'retiro' && (
                                <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                                  Retiro
                                </span>
                              )}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className={`font-medium ${
                                saving.transaction_type === 'deposito' ? 'text-green-600' : 'text-red-600'
                              }`}>
                                {saving.transaction_type === 'deposito' ? '+' : '-'}{formatCurrency(saving.amount)}
                              </span>
                              <button
                                onClick={() => handleOpenModal(saving)}
                                className="text-blue-600 hover:text-blue-700"
                              >
                                <Edit2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDelete(saving.id)}
                                className="text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </Card>
              ))
            )}
          </div>
        )}

        {/* Vista de lista */}
        {viewMode === 'list' && (
          <div className="space-y-3">
            {isLoading ? (
              <Card>
                <p className="text-center text-gray-500">Cargando ahorros...</p>
              </Card>
            ) : savings.length === 0 ? (
              <Card>
                <div className="text-center py-8">
                  <PiggyBank className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">No hay ahorros registrados</p>
                  <p className="text-sm text-gray-400">
                    Comienza registrando tu primer ahorro
                  </p>
                </div>
              </Card>
            ) : (
              savings.map((saving) => (
                <Card key={saving.id} className="hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <PiggyBank className={`w-5 h-5 ${
                          saving.transaction_type === 'deposito' ? 'text-green-600' : 'text-red-600'
                        }`} />
                        <h3 className="font-semibold text-gray-900 truncate">
                          {saving.purpose || 'Ahorro general'}
                        </h3>
                        {saving.transaction_type === 'retiro' && (
                          <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                            Retiro
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-500">
                        {format(new Date(saving.date), "d 'de' MMMM, yyyy", { locale: es })}
                      </p>
                      {saving.notes && (
                        <p className="text-sm text-gray-600 mt-1">{saving.notes}</p>
                      )}
                      {saving.goal_amount && (
                        <div className="mt-2">
                          <p className="text-xs text-gray-500">
                            Meta: {formatCurrency(saving.goal_amount)}
                          </p>
                        </div>
                      )}
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <p className={`text-lg font-bold ${
                        saving.transaction_type === 'deposito' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {saving.transaction_type === 'deposito' ? '+' : '-'}{formatCurrency(saving.amount)}
                      </p>
                      <div className="flex gap-1">
                        <button
                          onClick={() => handleOpenModal(saving)}
                          className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(saving.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </Card>
              ))
            )}
          </div>
        )}

        {/* Modal */}
        <Modal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          title={editingSaving ? 'Editar Ahorro' : 'Registrar Ahorro'}
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Fecha"
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
            />

            {/* Selector de tipo de transacción */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Tipo de movimiento
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, transaction_type: 'deposito' })}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    formData.transaction_type === 'deposito'
                      ? 'border-green-500 bg-green-50 text-green-700'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center gap-1">
                    <TrendingUp className="w-5 h-5" />
                    <span className="text-sm font-medium">Depósito</span>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, transaction_type: 'retiro' })}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    formData.transaction_type === 'retiro'
                      ? 'border-red-500 bg-red-50 text-red-700'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center gap-1">
                    <TrendingUp className="w-5 h-5 rotate-180" />
                    <span className="text-sm font-medium">Retiro</span>
                  </div>
                </button>
              </div>
            </div>

            {/* Selector de meta existente o nueva */}
            {!editingSaving && goals.length > 0 && (
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  ¿Agregar a una meta existente?
                </label>
                <Select
                  value={formData.purpose}
                  onChange={(e) => {
                    const selectedGoal = goals.find(g => g.purpose === e.target.value);
                    setFormData({ 
                      ...formData, 
                      purpose: e.target.value,
                      goal_amount: selectedGoal?.goalAmount || undefined
                    });
                  }}
                  options={goals.map(g => ({ value: g.purpose, label: g.purpose }))}
                  showAllOption
                  allOptionLabel="-- Crear nueva meta --"
                />
              </div>
            )}

            <Input
              label="Propósito / Meta"
              type="text"
              value={formData.purpose}
              onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
              placeholder="Ej: Auto nuevo, Vacaciones, Emergencias..."
              required
              helperText={!editingSaving && formData.purpose && goals.some(g => g.purpose === formData.purpose) ? `Agregando a la meta existente: ${formData.purpose}` : undefined}
            />

            <CurrencyInput
              label="Monto"
              value={formData.amount}
              onChange={(value) => setFormData({ ...formData, amount: value })}
              required
            />

            <CurrencyInput
              label="Meta de ahorro (opcional)"
              value={formData.goal_amount || 0}
              onChange={(value) => setFormData({ ...formData, goal_amount: value || undefined })}
              helperText={formData.purpose && goals.some(g => g.purpose === formData.purpose) 
                ? `Meta actual: ${formatCurrency(goals.find(g => g.purpose === formData.purpose)?.goalAmount || 0)}`
                : "Define cuánto quieres ahorrar en total para este propósito"}
            />

            <Textarea
              label="Notas"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="Detalles adicionales..."
              rows={3}
            />

            <div className="flex gap-3 pt-4">
              <Button
                type="button"
                variant="secondary"
                onClick={handleCloseModal}
                fullWidth
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                isLoading={isSubmitting}
                fullWidth
              >
                {editingSaving ? 'Actualizar' : 'Guardar'}
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </MobileLayout>
  );
}
