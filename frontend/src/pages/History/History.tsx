import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './History.module.css';
import { authService } from '@/api/authService';

interface HistoryRecord {
  id: number;
  created_at: string;
  result: number;
  result_label: string;
  probability: number;
  llm_feedback?: string;
  input_data: any;
  model_scores?: Record<string, any>;
}

const History = () => {
  const navigate = useNavigate();
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const response = await authService.getHistory();
      setRecords(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Błąd pobierania historii:', err);
      // If auth error, let protected route handle it or redirect
      if (err.message && (err.message.includes('zalogowany') || err.message.includes('sesja'))) {
        navigate('/logowanie');
        return;
      }
      setError(err.message || 'Nie udało się pobrać historii');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Czy na pewno chcesz usunąć ten rekord?')) {
      return;
    }

    try {
      await authService.deleteHistory(id);
      setRecords(records.filter(r => r.id !== id));
    } catch (err: any) {
      alert('Nie udało się usunąć rekordu: ' + err.message);
    }
  };

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pl-PL', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getResultColor = (probability: number): string => {
    if (probability < 15) {
      return styles.resultGreen;  // Niskie ryzyko
    } else if (probability < 35) {
      return styles.resultYellow;  // Średnie ryzyko
    } else {
      return styles.resultRed;  // Wysokie ryzyko
    }
  };

  const getRiskLevel = (probability: number): string => {
    if (probability < 15) {
      return 'Niskie ryzyko';
    } else if (probability < 35) {
      return 'Średnie ryzyko';
    } else {
      return 'Wysokie ryzyko';
    }
  };

  const getResultIcon = (probability: number): string => {
    if (probability < 15) {
      return '✓';
    } else if (probability < 35) {
      return '⚠';
    } else {
      return '⚠';
    }
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Ładowanie historii...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>
          <h2>Wystąpił błąd</h2>
          <p>{error}</p>
          <button className={styles.btnPrimary} onClick={() => navigate('/predyktor-ryzyka')}>
            Wykonaj nowy test
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Historia Twoich badań</h1>
            <p className={styles.subtitle}>
              Łącznie wykonałeś {records.length} {records.length === 1 ? 'test' : 'testów'}
            </p>
          </div>
          <button
            className={styles.btnPrimary}
            onClick={() => navigate('/predyktor-ryzyka')}
          >
            + Wykonaj nowy test
          </button>
        </div>

        {records.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>📊</div>
            <h2>Brak historii</h2>
            <p>Nie masz jeszcze żadnych zapisanych wyników.</p>
            <button
              className={styles.btnPrimary}
              onClick={() => navigate('/predyktor-ryzyka')}
            >
              Wykonaj pierwszy test
            </button>
          </div>
        ) : (
          <div className={styles.timeline}>
            {records.map((record, index) => (
              <div key={record.id} className={styles.timelineItem}>
                <div className={styles.timelineDot}></div>
                {index < records.length - 1 && <div className={styles.timelineLine}></div>}

                <div className={styles.card}>
                  <div className={styles.cardHeader}>
                    <div className={styles.cardHeaderLeft}>
                      <div className={`${styles.resultBadge} ${getResultColor(record.probability)}`}>
                        <span className={styles.resultIcon}>{getResultIcon(record.probability)}</span>
                        <span className={styles.resultLabel}>{getRiskLevel(record.probability)}</span>
                      </div>
                      <div className={styles.dateInfo}>
                        <span className={styles.dateIcon}>📅</span>
                        {formatDate(record.created_at)}
                      </div>
                    </div>
                    <div className={styles.cardHeaderRight}>
                      <div className={styles.probability}>
                        <span className={styles.probabilityValue}>{record.probability.toFixed(1)}%</span>
                        <span className={styles.probabilityLabel}>ryzyko</span>
                      </div>
                    </div>
                  </div>

                  {record.llm_feedback && (
                    <div className={styles.llmFeedback}>
                      <h4 className={styles.feedbackTitle}>💡 Zalecenia AI</h4>
                      <div className={styles.feedbackContent}>
                        {record.llm_feedback.split('\n').map((line, i) =>
                          line.trim() && <p key={i}>{line}</p>
                        )}
                      </div>
                    </div>
                  )}

                  <div className={styles.cardActions}>
                    <button
                      className={styles.btnExpand}
                      onClick={() => toggleExpand(record.id)}
                    >
                      {expandedId === record.id ? '▼ Zwiń szczegóły' : '▶ Pokaż szczegóły'}
                    </button>
                    <button
                      className={styles.btnDelete}
                      onClick={() => handleDelete(record.id)}
                    >
                      🗑️ Usuń
                    </button>
                  </div>

                  {expandedId === record.id && (
                    <div className={styles.expandedContent}>

                      {/* NEW: Model Comparison Section */}
                      {record.model_scores && (
                        <div className={styles.modelsComparison}>
                          <h4 className={styles.detailsTitle}>Szczegóły modeli</h4>
                          <div className={styles.modelsGrid}>
                            {Object.entries(record.model_scores).map(([modelName, data]: [string, any]) => {
                              if (!data) return null;
                              const risk = data.diabetes_risk ||
                                (data.probabilities.class_1 + data.probabilities.class_2);

                              const getModelLabel = (name: string) => {
                                if (name === 'gradient_boost') return 'Gradient Boosting (Główny)';
                                if (name === 'logistic') return 'Regresja Logistyczna';
                                if (name === 'random_forest') return 'Random Forest';
                                return name;
                              }

                              return (
                                <div key={modelName} className={styles.modelItem}>
                                  <div className={styles.modelName}>{getModelLabel(modelName)}</div>
                                  <div className={styles.modelRisk}>
                                    <span className={styles.riskValue}>{risk.toFixed(1)}%</span>
                                    <span className={styles.riskLabel}> ryzyka</span>
                                  </div>
                                </div>
                              )
                            })}
                          </div>
                        </div>
                      )}

                      <h4 className={styles.detailsTitle}>Dane wejściowe</h4>
                      <div className={styles.detailsGrid}>
                        {record.input_data.BMI && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>BMI:</span>
                            <span className={styles.detailValue}>{record.input_data.BMI.toFixed(1)}</span>
                          </div>
                        )}
                        {record.input_data.Age !== undefined && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Wiek:</span>
                            <span className={styles.detailValue}>Kategoria {record.input_data.Age}</span>
                          </div>
                        )}
                        {record.input_data.HighBP !== undefined && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Wysokie ciśnienie:</span>
                            <span className={styles.detailValue}>{record.input_data.HighBP ? 'Tak' : 'Nie'}</span>
                          </div>
                        )}
                        {record.input_data.HighChol !== undefined && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Wysoki cholesterol:</span>
                            <span className={styles.detailValue}>{record.input_data.HighChol ? 'Tak' : 'Nie'}</span>
                          </div>
                        )}
                        {record.input_data.Smoker !== undefined && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Palenie:</span>
                            <span className={styles.detailValue}>{record.input_data.Smoker ? 'Tak' : 'Nie'}</span>
                          </div>
                        )}
                        {record.input_data.PhysActivity !== undefined && (
                          <div className={styles.detailItem}>
                            <span className={styles.detailLabel}>Aktywność fizyczna:</span>
                            <span className={styles.detailValue}>{record.input_data.PhysActivity ? 'Tak' : 'Nie'}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default History;