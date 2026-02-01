import { useParams, useNavigate } from 'react-router-dom';
import { ML_PERSONAS } from '../../constants/personas';
import styles from './PersonaDetail.module.css';

const doctorImages: Record<string, string> = {
  logistic: '/dr-andrzej.jpg',
  random_forest: '/dr-jolanta.jpg',
  gradient_boost: '/dr-pawel.jpg',
};

const PersonaDetail = () => {
  const { personaId } = useParams<{ personaId: string }>();
  const navigate = useNavigate();

  const persona = personaId && ML_PERSONAS[personaId];
  const doctorImage = personaId && doctorImages[personaId];

  if (!persona) {
    return (
      <div className={styles.container}>
        <div className={styles.content}>
          <h1>Persona nie znaleziona</h1>
          <button 
            className={styles.btnBack}
            onClick={() => navigate(-1)}
          >
            Powrót
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <button 
          className={styles.btnBack}
          onClick={() => navigate(-1)}
        >
          ← Powrót do wyników
        </button>

        <div className={styles.heroSection}>
          <div className={styles.imagePlaceholder}>
            {doctorImage ? (
              <img src={doctorImage} alt={persona.name} className={styles.doctorImage} />
            ) : (
              <div className={styles.imagePlaceholderText}>
                Miejsce na zdjęcie lekarza
              </div>
            )}
          </div>

          <div className={styles.heroContent}>
            <h1 className={styles.personaName}>{persona.name}</h1>
            <p className={styles.personaModel}>{persona.model}</p>
            <p className={styles.personaTitle}>{persona.title}</p>
            <p className={styles.personaDescription}>
              {persona.description}
            </p>
          </div>
        </div>

        <div className={styles.detailsSection}>
          <div className={styles.strengthsCard}>
            <h2 className={styles.cardTitle}>Jego siła</h2>
            <ul className={styles.strengthsList}>
              {persona.strengths.map((strength, idx) => (
                <li key={idx} className={styles.strengthItem}>
                  <span className={styles.strengthIcon}>•</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className={styles.whenCard}>
            <h2 className={styles.cardTitle}>
              {personaId === 'random_forest' ? 'Kiedy jej słuchać?' : 'Kiedy go słuchać?'}
            </h2>
            <p className={styles.whenText}>
              {persona.whenToListen}
            </p>
          </div>

          <div className={styles.limitationsCard}>
            <h2 className={styles.cardTitle}>⚠️ Ograniczenia</h2>
            <p className={styles.limitationsText}>
              {persona.limitations}
            </p>
          </div>
        </div>

        <div className={styles.ctaSection}>
          <button 
            className={styles.btnPrimary}
            onClick={() => navigate(-1)}
          >
            Wróć do analizy
          </button>
        </div>
      </div>
    </div>
  );
};

export default PersonaDetail;
