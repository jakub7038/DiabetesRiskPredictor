import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import styles from './PredictionResult.module.css';
import { ML_PERSONAS } from '../../constants/personas';

interface ModelPrediction {
  confidence: number;
  prediction: number;
  diabetes_risk?: number;
  probabilities: {
    class_0: number;
    class_1: number;
    class_2: number;
  };
}

interface PredictionData {
  predictions: {
    logistic?: ModelPrediction;
    random_forest?: ModelPrediction;
    gradient_boost?: ModelPrediction;
    llm_analysis?: string;
    shap_factors?: string[];
  };
  is_saved: boolean;
}

const PredictionResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState<PredictionData | null>(null);

  useEffect(() => {
    if (location.state?.result) {
      setData(location.state.result);
    } else {
      navigate('/predyktor-ryzyka');
    }
  }, [location, navigate]);

  if (!data) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Ładowanie wyników...</div>
      </div>
    );
  }

  const getResultLabel = (prediction: number): string => {
    switch (prediction) {
      case 0:
        return 'Brak cukrzycy';
      case 1:
        return 'Stan przedcukrzycowy';
      case 2:
        return 'Cukrzyca';
      default:
        return 'Nieznany';
    }
  };

  const getResultColorFromRisk = (diabetesRisk: number): string => {
    if (diabetesRisk < 15) {
      return styles.resultGreen;
    } else if (diabetesRisk < 35) {
      return styles.resultYellow;
    } else {
      return styles.resultRed;
    }
  };

  const getRiskLevelFromProbability = (diabetesRisk: number): string => {
    if (diabetesRisk < 15) {
      return 'Niskie ryzyko';
    } else if (diabetesRisk < 35) {
      return 'Średnie ryzyko';
    } else {
      return 'Wysokie ryzyko';
    }
  };

  const getResultIcon = (diabetesRisk: number): string => {
    if (diabetesRisk < 15) {
      return '✓';
    } else if (diabetesRisk < 35) {
      return '⚠';
    } else {
      return '⚠';
    }
  };

  const { predictions, is_saved } = data;
  const mainPrediction = predictions.gradient_boost || predictions.random_forest || predictions.logistic;

  // Oblicz prawdziwe ryzyko cukrzycy
  const diabetesRisk = mainPrediction?.diabetes_risk || 
                       (mainPrediction ? 
                         mainPrediction.probabilities.class_1 + mainPrediction.probabilities.class_2 
                         : 0);
  
  const riskLevelText = getRiskLevelFromProbability(diabetesRisk);

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>Wyniki Twojej analizy</h1>
          {is_saved && (
            <div className={styles.savedBadge}>
              <span>💾</span> Wynik zapisany w historii
            </div>
          )}
        </div>

        {/* Main Result Card */}
        {mainPrediction && (
          <div className={`${styles.mainResult} ${getResultColorFromRisk(diabetesRisk)}`}>
            <div className={styles.resultIcon}>
              {getResultIcon(diabetesRisk)}
            </div>
            <div className={styles.resultContent}>
              <h2 className={styles.resultTitle}>
                {riskLevelText}
              </h2>
              <div className={styles.confidence}>
                Ryzyko cukrzycy: <strong>{diabetesRisk.toFixed(1)}%</strong>
              </div>
            </div>
          </div>
        )}

        {/* Model Predictions */}
        <div className={styles.modelsSection}>
          <h3 className={styles.sectionTitle}>Wyniki z poszczególnych modeli</h3>
          <div className={styles.modelsGrid}>
            {predictions.logistic && (
              <ModelCard
                data={predictions.logistic}
                modelKey="logistic"
              />
            )}
            {predictions.random_forest && (
              <ModelCard
                data={predictions.random_forest}
                modelKey="random_forest"
              />
            )}
            {predictions.gradient_boost && (
              <ModelCard
                data={predictions.gradient_boost}
                modelKey="gradient_boost"
              />
            )}
          </div>
        </div>

        {/* SHAP Factors - only for logged users */}
        {predictions.shap_factors && predictions.shap_factors.length > 0 && (
          <div className={styles.shapSection}>
            <h3 className={styles.sectionTitle}>Główne czynniki wpływające na wynik</h3>
            <div className={styles.factorsList}>
              {predictions.shap_factors.map((factor, index) => (
                <div key={index} className={styles.factorItem}>
                  <span className={styles.factorBullet}>•</span>
                  <span className={styles.factorText}>{factor}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* LLM Analysis - only for logged users */}
        {predictions.llm_analysis && (
          <div className={styles.llmSection}>
            <h3 className={styles.sectionTitle}>Spersonalizowane zalecenia</h3>
            <div className={styles.llmContent}>
              {predictions.llm_analysis.split('\n').map((line, index) => {
                if (line.trim()) {
                  return <p key={index} className={styles.llmParagraph}>{line}</p>;
                }
                return null;
              })}
            </div>
          </div>
        )}

        {/* Call to Action */}
        <div className={styles.ctaSection}>
          {diabetesRisk >= 35 && (
            <div className={styles.warningBox}>
              <p>
                <strong>⚠️ Ważne:</strong> Ten test ma charakter informacyjny i nie stanowi diagnozy medycznej. 
                Zalecamy konsultację z lekarzem w celu wykonania profesjonalnych badań krwi.
              </p>
            </div>
          )}

          <div className={styles.buttonGroup}>
            <button
              className={styles.btnPrimary}
              onClick={() => navigate('/predyktor-ryzyka')}
            >
              Wykonaj nowy test
            </button>
            {is_saved && (
              <button
                className={styles.btnSecondary}
                onClick={() => navigate('/historia')}
              >
                Zobacz historię
              </button>
            )}
            {!is_saved && (
              <button
                className={styles.btnSecondary}
                onClick={() => navigate('/rejestracja')}
              >
                Zarejestruj się, aby zapisywać wyniki
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper Component
interface ModelCardProps {
  data: ModelPrediction;
  modelKey?: string;
}

const ModelCard = ({ data, modelKey }: ModelCardProps) => {
  const navigate = useNavigate();

  const getResultLabel = (prediction: number): string => {
    switch (prediction) {
      case 0: return 'Brak cukrzycy';
      case 1: return 'Stan przedcukrzycowy';
      case 2: return 'Cukrzyca';
      default: return 'Nieznany';
    }
  };

  // Get persona for this model
  const persona = modelKey && ML_PERSONAS[modelKey];
  const displayName = persona ? `${persona.name} (${persona.model})` : 'Model';

  // Oblicz prawdziwe ryzyko cukrzycy (klasa 1 + klasa 2)
  const diabetesRisk = data.diabetes_risk || 
                       (data.probabilities.class_1 + data.probabilities.class_2);

  const handleLearnMore = () => {
    if (modelKey) {
      navigate(`/persona/${modelKey}`);
    }
  };

  return (
    <div className={styles.modelCard}>
      <div className={styles.modelHeader}>
        <h4 className={styles.modelName}>{displayName}</h4>
      </div>

      <div className={styles.modelResult}>
        <div className={styles.modelPrediction}>
          {getResultLabel(data.prediction)}
        </div>
        <div className={styles.modelConfidence}>
          {diabetesRisk.toFixed(1)}%
        </div>
      </div>
      <p style={{ fontSize: '0.8rem', color: '#6b7280', marginBottom: '1rem', textAlign: 'center' }}>
        Ryzyko cukrzycy (klasa 1 + klasa 2)
      </p>
      <div className={styles.probabilities}>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Brak cukrzycy</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probGreen}`}
              style={{ width: `${data.probabilities.class_0}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_0.toFixed(1)}%</div>
        </div>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Przedcukrzycowy</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probYellow}`}
              style={{ width: `${data.probabilities.class_1}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_1.toFixed(1)}%</div>
        </div>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Cukrzyca</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probRed}`}
              style={{ width: `${data.probabilities.class_2}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_2.toFixed(1)}%</div>
        </div>
      </div>

      {modelKey && (
        <button 
          className={styles.learnMoreBtn}
          onClick={handleLearnMore}
        >
          Poznaj {persona?.name}
        </button>
      )}
    </div>
  );
};

export default PredictionResult;