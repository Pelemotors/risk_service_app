import React, { useState } from 'react';

const RiskRuleForm: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    rule_json: '',
    weight: 1.0,
    is_active: true,
  });

  const [response, setResponse] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const target = e.target as HTMLInputElement;
    const { name, value, type } = target;
    const checked = type === 'checkbox' ? target.checked : undefined;

    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5001/api/risk_rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.success) {
        setResponse('✅ כלל נשמר בהצלחה');
      } else {
        setResponse('❌ שגיאה: ' + (data.message || data.error));
      }
    } catch (error: any) {
      setResponse('❌ שגיאה כללית: ' + error.message);
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white mt-10 rounded-xl shadow-md p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-2">📋 יצירת כלל סיכון</h2>
      <p className="text-gray-600 mb-6">
        כאן תוכל להגדיר כלל לחישוב הסיכון במערכת, לדוגמה:
        <code className="block bg-gray-100 p-2 rounded mt-2 text-sm font-mono">
          {"{\"if\": {\"age\": \"<25\"}, \"then\": {\"risk\": \"high\"}}"}
        </code>
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-semibold">שם הכלל *</label>
          <input
            name="name"
            placeholder="לדוגמה: גיל נמוך"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        <div>
          <label className="block mb-1 font-semibold">תיאור (לא חובה)</label>
          <textarea
            name="description"
            placeholder="מה הכלל בודק בפועל"
            value={formData.description}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        <div>
          <label className="block mb-1 font-semibold">JSON של הכלל *</label>
          <textarea
            name="rule_json"
            placeholder='{"if": ..., "then": ...}'
            value={formData.rule_json}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded p-2 font-mono text-sm"
            rows={6}
          />
        </div>

        <div>
          <label className="block mb-1 font-semibold">משקל (weight)</label>
          <input
            name="weight"
            type="number"
            step="0.1"
            value={formData.weight}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        <div className="flex items-center space-x-2">
          <input
            name="is_active"
            type="checkbox"
            checked={formData.is_active}
            onChange={handleChange}
          />
          <label>האם הכלל פעיל</label>
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white py-2 px-6 rounded hover:bg-blue-700"
        >
          💾 שמור כלל
        </button>

        {response && (
          <div className="mt-4 p-2 rounded bg-gray-100 text-center">{response}</div>
        )}
      </form>
    </div>
  );
};

export default RiskRuleForm;
