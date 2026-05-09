import { useState } from 'react';
import axios from 'axios';

export function MlPredict() {
  const [features, setFeatures] = useState('');
  const [prediction, setPrediction] = useState<number | null>(null);
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('Прогнозирование...');
    try {
      const featuresArray = features.split(',').map((v) => parseFloat(v.trim()));
      const response = await axios.post('/api/v1/models/predict', { features: featuresArray });
      if (response.status === 200) {
        setPrediction(response.data.prediction);
        setStatus('Готово');
      } else {
        setStatus('Ошибка');
      }
    } catch (err) {
      setStatus('Ошибка: ' + (err as Error).message);
      setPrediction(null);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '15px 0', borderRadius: '8px' }}>
      <h2>ML прогноз (сумма признаков)</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Введите числа через запятую (например 1,2,3,4): </label>
          <input value={features} onChange={(e) => setFeatures(e.target.value)} required style={{ width: '300px' }} />
        </div>
        <button type="submit">Предсказать</button>
      </form>
      {prediction !== null && <p><strong>Прогноз: {prediction}</strong></p>}
      <p>{status}</p>
    </div>
  );
}