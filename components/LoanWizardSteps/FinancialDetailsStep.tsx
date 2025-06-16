//C:\GAL\financing\risk-ui\src\components\LoanWizardSteps\FinancialDetailsStep.tsx
import { useFormContext } from 'react-hook-form';
import { useState } from 'react';

const banks = [
  { code: '4', name: 'בנק יהב' },
  { code: '9', name: 'בנק הדואר' },
  { code: '10', name: 'בנק לאומי' },
  { code: '11', name: 'בנק דיסקונט' },
  { code: '12', name: 'בנק הפועלים' },
  { code: '13', name: 'בנק אגוד' },
  { code: '14', name: 'בנק אוצר החייל' },
  { code: '17', name: 'בנק מרכנתיל' },
  { code: '20', name: 'בנק מזרחי טפחות' },
  { code: '22', name: 'Citibank N.A' },
  { code: '23', name: 'HSBC' },
  { code: '26', name: 'יובנק' },
  { code: '27', name: 'Barclays Bank' },
  { code: '30', name: 'בנק למסחר' },
  { code: '31', name: 'הבנק הבינלאומי' },
  { code: '34', name: 'בנק ערבי ישראלי' },
  { code: '39', name: 'State Bank of India' },
  { code: '46', name: 'בנק מסד' },
  { code: '50', name: 'מרכז סליקה בנקאי' },
  { code: '52', name: 'בנק פועלי אגודת ישראל' },
  { code: '54', name: 'בנק ירושלים' },
  { code: '59', name: 'שב"א' },
  { code: '65', name: 'קופת חיסכון לחינוך' },
  { code: '68', name: 'בנק דקסיה' },
  { code: '99', name: 'בנק ישראל' },
];

export default function FinancialDetailsStep() {
  const { register, setValue } = useFormContext();
  const [searchTerm, setSearchTerm] = useState('');
  const filteredBanks = banks.filter(b =>
    b.name.includes(searchTerm) || b.code.includes(searchTerm)
  );

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">פרטים פיננסיים</h3>

      <div>
        <label className="block mb-1">בחר בנק לפי שם או קוד:</label>
        <input
          className="w-full border p-2 rounded mb-2"
          placeholder="הקלד שם בנק או מספר"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <ul className="border rounded max-h-32 overflow-y-auto bg-white">
          {filteredBanks.map((bank) => (
            <li
              key={bank.code}
              className="p-2 hover:bg-blue-100 cursor-pointer"
              onClick={() => {
                setValue('bank_name', bank.name);
                setValue('bank_code', bank.code);
                setSearchTerm(bank.name);
              }}
            >
              {bank.code} - {bank.name}
            </li>
          ))}
        </ul>
      </div>

      <input {...register('bank_name')} type="hidden" />
      <input {...register('bank_code')} type="hidden" />

      <input {...register('branch_number')} className="w-full border p-2 rounded" placeholder="מספר סניף (3 ספרות)" maxLength={3} />
      <input {...register('account_number')} className="w-full border p-2 rounded" placeholder="מספר חשבון (עד 15 תווים)" maxLength={15} />
    </div>
  );
}
