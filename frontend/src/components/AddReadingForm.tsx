import { useState } from 'react';
import axios from 'axios';

export function AddReadingForm() {
  const [sensorId, setSensorId] = useState('');
  const [value, setValue] = useState('');
  const [timestamp, setTimestamp] = useState('');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('Отправка...');
    try {
      const payload = {
        sensor_id: sensorId,
        value: parseFloat(value),
        timestamp: timestamp,
        location: { lat: parseFloat(lat), lon: parseFloat(lon) }
      };
      const response = await axios.post('/api/v1/sensors/readings', payload);
      if (response.status === 201) {
        setStatus('Успешно добавлено!');
        // Очистить форму
        setSensorId('');
        setValue('');
        setTimestamp('');
        setLat('');
        setLon('');
        // Обновить страницу, чтобы график показал новые данные
        setTimeout(() => window.location.reload(), 500);
      } else {
        setStatus('Ошибка при добавлении');
      }
    } catch (err) {
      setStatus('Ошибка: ' + (err as Error).message);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', margin: '15px 0', borderRadius: '8px' }}>
      <h2>Добавить новое показание</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Sensor ID (мин. 36 символов): </label>
          <input value={sensorId} onChange={(e) => setSensorId(e.target.value)} required minLength={36} style={{ width: '300px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Значение: </label>
          <input type="number" step="any" value={value} onChange={(e) => setValue(e.target.value)} required />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Timestamp (ISO, например 2026-05-09T12:00:00Z): </label>
          <input value={timestamp} onChange={(e) => setTimestamp(e.target.value)} required style={{ width: '300px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Широта (lat): </label>
          <input type="number" step="any" value={lat} onChange={(e) => setLat(e.target.value)} required />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Долгота (lon): </label>
          <input type="number" step="any" value={lon} onChange={(e) => setLon(e.target.value)} required />
        </div>
        <button type="submit">Отправить</button>
      </form>
      <p>{status}</p>
    </div>
  );
}