import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useForm, FormProvider } from 'react-hook-form';

import RiskRuleForm from './components/RiskRuleForm';
import LoanApplicationWizard from './components/LoanApplicationWizard';

function App() {
  const methods = useForm();

  return (
    <FormProvider {...methods}>
      <Router>
        <div className="min-h-screen bg-gray-100 p-6">
          <Routes>
            {/* ברירת מחדל תוביל לטופס הבקשה */}
            <Route path="/" element={<Navigate to="/loan" replace />} />

            {/* טופס בקשה */}
            <Route path="/loan" element={<LoanApplicationWizard />} />
            <Route path="/loan-request" element={<LoanApplicationWizard />} />

            {/* ניהול כללי סיכון */}
            <Route path="/risk-rules" element={<RiskRuleForm />} />
          </Routes>
        </div>
      </Router>
    </FormProvider>
  );
}

export default App;
