//C:\GAL\financing\risk-ui\src\components\LoanWizardSteps\FinalStep.tsx
import { useFormContext } from 'react-hook-form';
import { useEffect, useState } from 'react';

type RiskResponse = {
  approved_amount: number;
  max_installments: number;
  max_percent: number;
  risk_tier: string;
};

export default function FinalStep() {
  const { getValues } = useFormContext();
  const [result, setResult] = useState<RiskResponse | null>(null);
  const [chosenInstallments, setChosenInstallments] = useState(60);
  const [monthlyPayment, setMonthlyPayment] = useState(0);

  useEffect(() => {
    const formData = getValues();

    fetch('http://localhost:5001/api/risk/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
      .then((res) => res.json())
      .then((data: RiskResponse) => {
        setResult(data);
        setChosenInstallments(data.max_installments);
      })
      .catch((err) => {
        console.error("❌ שגיאה בקבלת תוצאה ממנוע סיכון:", err);
      });
  }, []);

  useEffect(() => {
    if (result) {
      const r = 0.099 / 12; // ריבית חודשית (9.9% שנתי)
      const n = chosenInstallments;
      const P = result.approved_amount;
      const monthly = (P * r) / (1 - Math.pow(1 + r, -n));
      setMonthlyPayment(Math.round(monthly));
    }
  }, [result, chosenInstallments]);

  if (!result) return <div>טוען אישור עקרוני...</div>;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-center">🟢 אישור עקרוני</h3>

      <div className="bg-green-100 p-4 rounded text-right">
        <p>💰 סכום מאושר: <strong>{result.approved_amount.toLocaleString()} ₪</strong></p>
        <p>📈 אחוז מימון מרבי: <strong>{result.max_percent}%</strong></p>
        <p>📆 עד {result.max_installments} תשלומים</p>
      </div>

      <div className="pt-4">
        <label className="block mb-2 text-right">בחר מספר תשלומים לסימולציה:</label>
        <select
          className="w-full border p-2 rounded text-right"
          value={chosenInstallments}
          onChange={(e) => setChosenInstallments(Number(e.target.value))}
        >
          {[12, 24, 36, 48, 60, 72, 84, 96, 100]
            .filter(n => n <= result.max_installments)
            .map((n) => (
              <option key={n} value={n}>{n} תשלומים</option>
            ))}
        </select>

        <p className="mt-4 text-center text-lg">
          💳 תשלום חודשי משוער: <strong>{monthlyPayment.toLocaleString()} ₪</strong>
        </p>
      </div>
    </div>
  );
}
