//C:\GAL\financing\risk-ui\src\components\LoanApplicationWizard.tsx
'use client';

import { useForm, FormProvider } from 'react-hook-form';
import { useState } from 'react';

import PersonalDetailsStep from './LoanWizardSteps/PersonalDetailsStep';
import FinancialDetailsStep from './LoanWizardSteps/FinancialDetailsStep';
import VehicleDetailsStep from './LoanWizardSteps/VehicleDetailsStep';
import FinancingDetailsStep from './LoanWizardSteps/FinancingDetailsStep';
import FinalStep from './LoanWizardSteps/FinalStep'; // ✅ הוספה

type WizardStep = 1 | 2 | 3 | 4 | 5;

export default function LoanApplicationWizard() {
  const methods = useForm({ mode: 'onTouched' });
  const [step, setStep] = useState<WizardStep>(1);

  const nextStep = () => setStep((prev) => (prev + 1 > 5 ? 5 : (prev + 1) as WizardStep));
  const prevStep = () => setStep((prev) => (prev - 1 < 1 ? 1 : (prev - 1) as WizardStep));

  const onSubmit = (data: any) => {
    console.log("📦 נתוני טופס:", data);
    nextStep();
  };

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={methods.handleSubmit(onSubmit)}
        className="max-w-3xl mx-auto p-6 bg-white shadow rounded space-y-6 text-right"
        dir="rtl"
      >
        <h2 className="text-2xl font-bold text-center">בקשת מימון לרכב</h2>

        {step === 1 && <PersonalDetailsStep />}
        {step === 2 && <FinancialDetailsStep />}
        {step === 3 && <VehicleDetailsStep />}
        {step === 4 && <FinancingDetailsStep />}
        {step === 5 && <FinalStep />}

        <div className="flex justify-between">
          {step > 1 ? (
            <button
              type="button"
              onClick={prevStep}
              className="px-4 py-2 bg-gray-200 rounded"
            >
              הקודם
            </button>
          ) : (
            <div />
          )}

          {step < 5 ? (
            <button
              type="button"
              onClick={nextStep}
              className="px-4 py-2 bg-blue-600 text-white rounded"
            >
              הבא
            </button>
          ) : (
            <button
              type="submit"
              className="px-4 py-2 bg-green-600 text-white rounded"
            >
              הגש בקשה
            </button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}
