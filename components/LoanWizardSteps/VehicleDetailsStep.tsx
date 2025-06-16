//C:\GAL\financing\risk-ui\src\components\LoanWizardSteps\VehicleDetailsStep.tsx
import { useFormContext } from 'react-hook-form';

export const manufacturers: string[] = [
  "Denza / דנזה",
  "EVEASY",
  "RAM / ראם",
  "XPENG",
  "ZEEKR",
  "אאודי",
  "אבארט",
  "אוטוביאנקי",
  "אולדסמוביל",
  "אוסטין",
  "אופל",
  "אורה / Ora",
  "איווייס",
  "איווקו",
  "אינפיניטי",
  "איסוזו",
  "אל.אי.וי.סי / LEVC",
  "אל.טי.איי",
  "אלפא רומיאו",
  "אלפין / ALPINE",
  "אם. ג'י. / MG",
  "אסטון מרטין",
  "אף. אי. דאבליו / FEW",
  "ב.מ.וו",
  "בי.ווי.די / BYD",
  "ביואיק",
  "בנטלי",
  "ג'אקו / Jaecoo",
  "ג'י.איי.סי / GAC",
  "ג'י.אם.סי / GMC",
  "ג'יאו / Geo",
  "ג'יאיוואן / Jiayuan",
  "ג'יי.איי.סי / JAC",
  "ג'ילי / Geely",
  "ג'יפ / Jeep",
  "ג'יפ תע''ר",
  "ג'נסיס",
  "גרייט וול",
  "דאצ'יה",
  "דודג'",
  "דונגפנג",
  "די.אס / DS",
  "דייהו",
  "דייהטסו",
  "האמר",
  "הונגצ'י / HONGQI",
  "הונדה",
  "הינו / HINO",
  "ווי / WEY",
  "וויה / VOYAH",
  "וולוו",
  "טאטא",
  "טויוטה",
  "טסלה",
  "יגואר",
  "יונדאי",
  "לאדה",
  "לינק&קו / Lynk&Co",
  "לינקולן",
  "ליפמוטור / Leapmotor",
  "ליצ'י",
  "למבורגיני",
  "לנד רובר",
  "לנצ'יה",
  "לקסוס",
  "מאזדה",
  "מאן",
  "מזראטי",
  "מיני",
  "מיצובישי",
  "מקלארן / McLaren",
  "מקסוס",
  "מרצדס",
  "ניאו / NIO",
  "ניסאן",
  "ננג'ינג",
  "סאאב",
  "סאן ליוינג / Sun Living",
  "סאנגיונג",
  "סאנשיין",
  "סובארו",
  "סוזוקי",
  "סיאט",
  "סיטרואן",
  "סמארט",
  "סנטרו",
  "סקודה",
  "סקייוול",
  "סרס / SERES",
  "פולסטאר / POLESTAR",
  "פולקסווגן",
  "פונטיאק",
  "פורד",
  "פורשה",
  "פורתינג / FORTHING",
  "פיאג'ו",
  "פיאט",
  "פיג'ו",
  "פרארי",
  "צ'רי / Chery",
  "קאדילק",
  "קארמה / Karma",
  "קופרה",
  "קיה",
  "קרייזלר",
  "רובר",
  "רולס רויס / Rolls Royse",
  "רנו",
  "שברולט"
];

const origins = [
  'ללא', 'פרטי', 'ליסינג', 'השכרה', 'חברה', 'מדינת ישראל'
];

export default function VehicleDetailsStep() {
  const { register } = useFormContext();

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">פרטי רכב</h3>

      <select {...register('car_type')} className="w-full border p-2 rounded">
        <option value="">סיווג רכב</option>
        <option value="חדש">חדש</option>
        <option value="משומש">משומש</option>
      </select>

      <input {...register('license_number')} className="w-full border p-2 rounded" placeholder="מספר רכב" />

      <label className="block">תאריך עלייה לכביש (חודש ושנה):</label>
      <div className="flex gap-2">
        <input {...register('registration_month')} type="number" min="1" max="12" placeholder="חודש" className="w-1/2 border p-2 rounded" />
        <input {...register('registration_year')} type="number" placeholder="שנה" className="w-1/2 border p-2 rounded" />
      </div>

      <label className="block">יצרן:</label>
      <select {...register('manufacturer')} className="w-full border p-2 rounded">
        <option value="">בחר יצרן</option>
        {manufacturers.map((m) => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>

      <input {...register('model')} className="w-full border p-2 rounded" placeholder="דגם (הקלדה חופשית)" />
      <input {...register('levi_code')} className="w-full border p-2 rounded" placeholder="קוד דגם לוי יצחק" />
      <input {...register('kilometers')} className="w-full border p-2 rounded" placeholder='ק"מ' />
      <input {...register('previous_owners')} className="w-full border p-2 rounded" placeholder="מספר בעלים קודמים" />

      <label className="block">מקוריות:</label>
      <select {...register('origin')} className="w-full border p-2 rounded">
        {origins.map((o) => (
          <option key={o} value={o}>{o}</option>
        ))}
      </select>

      <input {...register('levi_price')} className="w-full border p-2 rounded" placeholder="מחיר מחירון" />
      <input {...register('sale_price')} className="w-full border p-2 rounded" placeholder="מחיר מכירה בפועל" />
    </div>
  );
}
