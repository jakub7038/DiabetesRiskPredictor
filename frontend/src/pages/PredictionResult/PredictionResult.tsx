import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import styles from './PredictionResult.module.css';

interface ModelPrediction {
  confidence: number;
  prediction: number;
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

  const getResultColor = (prediction: number): string => {
    switch (prediction) {
      case 0:
        return styles.resultGreen;
      case 1:
        return styles.resultYellow;
      case 2:
        return styles.resultRed;
      default:
        return '';
    }
  };

  const getResultIcon = (prediction: number): string => {
    switch (prediction) {
      case 0:
        return '✓';
      case 1:
        return '⚠';
      case 2:
        return '⚠';
      default:
        return '?';
    }
  };

  const { predictions, is_saved } = data;
  const mainPrediction = predictions.random_forest || predictions.logistic || predictions.gradient_boost;

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
          <div className={`${styles.mainResult} ${getResultColor(mainPrediction.prediction)}`}>
            <div className={styles.resultIcon}>
              {getResultIcon(mainPrediction.prediction)}
            </div>
            <div className={styles.resultContent}>
              <h2 className={styles.resultTitle}>
                {getResultLabel(mainPrediction.prediction)}
              </h2>
              <div className={styles.confidence}>
                Pewność: <strong>{mainPrediction.confidence}%</strong>
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
                name="Regresja Logistyczna"
                data={predictions.logistic}
              />
            )}
            {predictions.random_forest && (
              <ModelCard
                name="Random Forest"
                data={predictions.random_forest}
                isMain
              />
            )}
            {predictions.gradient_boost && (
              <ModelCard
                name="Gradient Boosting"
                data={predictions.gradient_boost}
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
          {mainPrediction && mainPrediction.prediction > 0 && (
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
  name: string;
  data: ModelPrediction;
  isMain?: boolean;
}

const ModelCard = ({ name, data, isMain }: ModelCardProps) => {
  const getResultLabel = (prediction: number): string => {
    switch (prediction) {
      case 0: return 'Brak cukrzycy';
      case 1: return 'Stan przedcukrzycowy';
      case 2: return 'Cukrzyca';
      default: return 'Nieznany';
    }
  };

  return (
    <div className={`${styles.modelCard} ${isMain ? styles.modelCardMain : ''}`}>
      <div className={styles.modelHeader}>
        <h4 className={styles.modelName}>{name}</h4>
        {isMain && <span className={styles.mainBadge}>Główny</span>}
      </div>
      <div className={styles.modelResult}>
        <div className={styles.modelPrediction}>
          {getResultLabel(data.prediction)}
        </div>
        <div className={styles.modelConfidence}>
          {data.confidence}%
        </div>
      </div>
      <div className={styles.probabilities}>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Brak cukrzycy</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probGreen}`}
              style={{ width: `${data.probabilities.class_0}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_0}%</div>
        </div>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Przedcukrzycowy</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probYellow}`}
              style={{ width: `${data.probabilities.class_1}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_1}%</div>
        </div>
        <div className={styles.probBar}>
          <div className={styles.probLabel}>Cukrzyca</div>
          <div className={styles.probBarOuter}>
            <div
              className={`${styles.probBarInner} ${styles.probRed}`}
              style={{ width: `${data.probabilities.class_2}%` }}
            />
          </div>
          <div className={styles.probValue}>{data.probabilities.class_2}%</div>
        </div>
      </div>
    </div>
  );
};

export default PredictionResult;