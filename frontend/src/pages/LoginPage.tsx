import { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Wallet, Mail, Lock } from 'lucide-react';
import { useAuthStore } from '../store/auth.store';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (error) {
      // Error manejado en el store
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo y título */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-600 text-white mb-4">
            <Wallet className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Control de Gastos
          </h1>
          <p className="text-gray-600">
            Gestiona tus finanzas personales de forma sencilla
          </p>
        </div>

        {/* Formulario */}
        <div className="card fade-in">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Iniciar Sesión
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-11 w-5 h-5 text-gray-400 pointer-events-none" />
                <Input
                  label="Correo electrónico"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="tu@email.com"
                  required
                  className="pl-10"
                />
              </div>

              <div className="relative">
                <Lock className="absolute left-3 top-11 w-5 h-5 text-gray-400 pointer-events-none" />
                <Input
                  label="Contraseña"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="pl-10"
                />
              </div>
            </div>

            <Button
              type="submit"
              fullWidth
              isLoading={isLoading}
              className="mt-6"
            >
              Iniciar Sesión
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              ¿No tienes cuenta?{' '}
              <Link
                to="/register"
                className="font-medium text-primary-600 hover:text-primary-700 transition-colors"
              >
                Regístrate aquí
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-8">
          Mantén tus finanzas bajo control 💰
        </p>
      </div>
    </div>
  );
}
