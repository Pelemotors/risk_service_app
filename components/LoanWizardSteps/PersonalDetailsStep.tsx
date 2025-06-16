//C:\GAL\financing\risk-ui\src\components\LoanWizardSteps\PersonalDetailsStep.tsx
import { useFormContext } from 'react-hook-form';
import { useState } from 'react';

export default function PersonalDetailsStep() {
  const { register } = useFormContext();
  const [showCoBorrower, setShowCoBorrower] = useState(false);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">לווה ראשי</h3>

      <input {...register('main_fullName')} className="w-full border p-2 rounded" placeholder="שם מלא" />
      <input {...register('main_idNumber')} className="w-full border p-2 rounded" placeholder="מספר ת.ז." />
      <input {...register('main_birthDate')} type="date" className="w-full border p-2 rounded" placeholder="תאריך לידה" />
      <input {...register('main_idIssueDate')} type="date" className="w-full border p-2 rounded" placeholder="תאריך הנפקת ת.ז." />
      <input {...register('main_phone')} className="w-full border p-2 rounded" placeholder="מספר טלפון נייד" />

      <label className="flex items-center gap-2 mt-4">
        <input
          type="checkbox"
          onChange={(e) => setShowCoBorrower(e.target.checked)}
        />
        יש לווה נוסף
      </label>

      {showCoBorrower && (
        <div className="space-y-3 border-t pt-4 mt-4">
          <h3 className="text-lg font-semibold">לווה נוסף</h3>
          <input {...register('co_fullName')} className="w-full border p-2 rounded" placeholder="שם מלא" />
          <input {...register('co_idNumber')} className="w-full border p-2 rounded" placeholder="מספר ת.ז." />
          <input {...register('co_birthDate')} type="date" className="w-full border p-2 rounded" placeholder="תאריך לידה" />
          <input {...register('co_idIssueDate')} type="date" className="w-full border p-2 rounded" placeholder="תאריך הנפקת ת.ז." />
          <input {...register('co_phone')} className="w-full border p-2 rounded" placeholder="מספר טלפון נייד" />
        </div>
      )}
    </div>
  );
}
