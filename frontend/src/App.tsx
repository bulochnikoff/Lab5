import { MetricChart } from './components/MetricChart';
import { AddReadingForm } from './components/AddReadingForm';
import { MlPredict } from './components/MlPredict';
import './App.css';

function App() {
  return (
    <div className="App">
      <header>
        <h1>Показания датчиков</h1>
      </header>
      <main>
        <AddReadingForm />
        <MetricChart />
        <MlPredict />
      </main>
    </div>
  );
}

export default App;