//C:\GAL\financing\risk-ui\src\components\LoanWizardSteps\FinancingDetailsStep.tsx

'use client';

import { useFormContext, Controller } from 'react-hook-form';

export default function FinancingDetailsStep() {
  const { register, watch, setValue, control } = useFormContext();
  const registrationYear = watch('registration_year');
  const carType = watch('car_type');
  const salePrice = Number(watch('sale_price') || 0);
  const financingAmount = Number(watch('financing_amount') || 0);

  const currentYear = new Date().getFullYear();
  const vehicleAge = currentYear - (registrationYear || currentYear);
  const isNewCar = carType === 'חדש';

  // החישוב של אחוז מימון מקסימלי
  const maxFinancingPercent = salePrice > 350_000 ? 90 : 100;
  const maxFinancingAmount = (salePrice * maxFinancingPercent) / 100;

  // קביעת אפשרויות מסלול לפי גיל הרכב
  const spitzerOptions = Array.from({ length: 81 }, (_, i) => 20 + i);
  let balloonOptions: number[] = [];

  if (isNewCar) {
    balloonOptions = [12, 24, 36, 48, 60];
  } else if (vehicleAge <= 3) {
    balloonOptions = [36, 60];
  } else if (vehicleAge <= 5) {
    balloonOptions = [36];
  }

  // תשלומי שפיצר לפי גיל
  let maxSpitzer = 60;
  if (isNewCar) maxSpitzer = 100;
  else if (vehicleAge === 2) maxSpitzer = 96;
  else if (vehicleAge === 3) maxSpitzer = 84;
  else if (vehicleAge === 4) maxSpitzer = 72;
  else if (vehicleAge === 5) maxSpitzer = 60;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">פרטי מימון</h3>

      <input
        {...register('financing_amount')}
        type="number"
        className="w-full border p-2 rounded"
        placeholder="סכום הלוואה מבוקש"
        max={maxFinancingAmount}
      />
      {salePrice > 0 && (
        <p className="text-sm text-gray-500">
          מקסימום מימון לפי מחיר מכירה: {maxFinancingPercent}% = {maxFinancingAmount.toLocaleString()} ₪
        </p>
      )}

      <label className="block">מסלול מימון:</label>
      <select {...register('financing_type')} className="w-full border p-2 rounded">
        <option value="שפיצר">שפיצר</option>
        {balloonOptions.length > 0 && <option value="בלון">בלון 40%</option>}
      </select>

      <label className="block">מספר תשלומים:</label>
      <Controller
        control={control}
        name="num_of_payments"
        render={({ field }) => (
          <select {...field} className="w-full border p-2 rounded">
            {(watch('financing_type') === 'בלון' ? balloonOptions : spitzerOptions.filter(m => m <= maxSpitzer)).map(n => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
        )}
      />

      <p className="text-sm text-gray-400">ריבית בסיס משוערת: 9.9% צמוד מדד</p>
    </div>
  );
}
