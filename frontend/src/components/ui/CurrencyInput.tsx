import type { InputHTMLAttributes } from 'react';
import { forwardRef, useState, useEffect } from 'react';

interface CurrencyInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'onChange' | 'value'> {
  label?: string;
  error?: string;
  helperText?: string;
  value: number;
  onChange: (value: number) => void;
}

const CurrencyInput = forwardRef<HTMLInputElement, CurrencyInputProps>(
  ({ label, error, helperText, value, onChange, className = '', ...props }, ref) => {
    const [displayValue, setDisplayValue] = useState('');
    const [isFocused, setIsFocused] = useState(false);

    useEffect(() => {
      // Solo actualizar si no está enfocado (para evitar conflictos con la edición)
      if (!isFocused) {
        if (value > 0) {
          setDisplayValue(value.toString());
        } else {
          setDisplayValue('');
        }
      }
    }, [value, isFocused]);

    const formatNumber = (num: number): string => {
      return num.toLocaleString('es-MX', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const input = e.target.value;
      
      // Remover todo excepto números y punto decimal
      const numbersOnly = input.replace(/[^\d.]/g, '');
      
      // Evitar múltiples puntos decimales
      const parts = numbersOnly.split('.');
      let cleanValue = parts[0];
      if (parts.length > 1) {
        cleanValue += '.' + parts.slice(1).join('').slice(0, 2);
      }
      
      // Actualizar el display value directamente
      setDisplayValue(cleanValue);
      
      // Convertir a número y notificar cambio
      const numValue = parseFloat(cleanValue) || 0;
      onChange(numValue);
    };

    const handleFocus = () => {
      setIsFocused(true);
      // Mostrar el valor sin formato cuando está en foco
      if (value > 0) {
        setDisplayValue(value.toString());
      }
    };

    const handleBlur = () => {
      setIsFocused(false);
      // Formatear cuando pierde el foco
      if (value > 0) {
        setDisplayValue(value.toString());
      }
    };

    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium pointer-events-none">
            $
          </span>
          <input
            ref={ref}
            type="text"
            inputMode="decimal"
            value={isFocused ? displayValue : (value > 0 ? formatNumber(value) : '')}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            className={`
              input pl-11
              ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {error && (
          <p className="mt-2 text-sm text-red-600">{error}</p>
        )}
        {helperText && !error && (
          <p className="mt-2 text-sm text-gray-500">{helperText}</p>
        )}
      </div>
    );
  }
);

CurrencyInput.displayName = 'CurrencyInput';

export default CurrencyInput;
