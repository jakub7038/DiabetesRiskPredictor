import React from 'react';
import styles from './UserProfile.module.css';
import HealthChat from '@/components/HealthChat/HealthChat'


interface UserData {
  firstName: string;
  lastName: string;
  age: number;
  height: number;
  weight: number;
  lastTestDate: string;
  lastRiskScore: number;
  riskLevel: 'Niskie' | 'Średnie' | 'Wysokie';
}

const currentUser: UserData = {
  firstName: "Jan",
  lastName: "Kowalski",
  age: 55,
  height: 176,
  weight: 92,
  lastTestDate: "2024-05-10", 
  lastRiskScore: 65,
  riskLevel: "Wysokie"
};

const UserProfile: React.FC = () => {

  const calculateBMI = (weight: number, height: number): number => {
    const heightInMeters = height / 100;
    return parseFloat((weight / (heightInMeters * heightInMeters)).toFixed(1));
  };

  const getDaysSinceTest = (dateString: string): number => {
    const testDate = new Date(dateString);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - testDate.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
  };

  const bmi = calculateBMI(currentUser.weight, currentUser.height);
  const daysSince = getDaysSinceTest(currentUser.lastTestDate);
  const isBmiHigh = bmi >= 25;

  return (
    <div className={styles.profileContainer}>
      <header className={styles.profileHeader}>
        <h1>Witaj, {currentUser.firstName}!</h1>
        <p>Twoje centrum monitorowania zdrowia</p>
      </header>

      <div className={styles.dashboardGrid}>
        {/* Karta 1: Główny Wynik Ryzyka */}

        <div className={styles.card}>
            <div className={styles.cardHeaderRow}>
            <h3>Twoje Dane</h3>
            <button className={styles.editLink} onClick={() => console.log("Edycja...")}>Edytuj</button>
            </div>
            
            <ul className={styles.detailsList}>
                <li className={styles.detailRow}>
                    <span className={styles.detailLabel}>Imię i nazwisko:</span>
                    <span className={styles.detailValue}>{currentUser.firstName} {currentUser.lastName}</span>
                </li>
                <li className={styles.detailRow}>
                    <span className={styles.detailLabel}>Wiek:</span>
                    <span className={styles.detailValue}>{currentUser.age} lat</span>
                </li>
                <li className={styles.detailRow}>
                    <span className={styles.detailLabel}>Płeć:</span>
                    <span className={styles.detailValue}>Mężczyzna</span> {/* Tu w przyszłości pobierzesz z user.gender */}
                </li>
                <li className={styles.detailRow}>
                    <span className={styles.detailLabel}>Wzrost:</span>
                    <span className={styles.detailValue}>{currentUser.height} cm</span>
                </li>
                <li className={styles.detailRow}>
                    <span className={styles.detailLabel}>Waga:</span>
                    <span className={styles.detailValue}>{currentUser.weight} kg</span>
                </li>
            </ul>
        </div>

        <div className={styles.card}>
          <h3>Twoje ryzyko cukrzycy</h3>
          <div className={styles.riskIndicator}>
            {/* Warunkowa klasa dla koloru tekstu */}
            <span className={`${styles.riskValue} ${currentUser.riskLevel === 'Wysokie' ? styles.textWarning : ''}`}>
              {currentUser.riskLevel}
            </span>
            <div className={styles.progressBarBg}>
              <div 
                className={styles.progressBarFill} 
                style={{ width: `${currentUser.lastRiskScore}%` }}
              ></div>
            </div>
            <p className={styles.scoreDetails}>{currentUser.lastRiskScore}% w skali ryzyka</p>
          </div>
        </div>

        {/* Karta 2: Czas od ostatniego badania */}
        <div className={styles.card}>
          <h3>Ostatnie badanie</h3>
          <div className={styles.daysDisplay}>
            <span className={styles.daysNumber}>{daysSince}</span>
            <span className={styles.daysLabel}>dni temu</span>
          </div>
          <p className={styles.dateSubtext}>Data: {currentUser.lastTestDate}</p>
        </div>

        {/* Karta 3: BMI z Ostrzeżeniem - Złożona klasa warunkowa */}
        <div className={`${styles.card} ${styles.bmiCard} ${isBmiHigh ? styles.warningBorder : ''}`}>
          <h3>Twoje BMI</h3>
          <div className={styles.bmiValue}>{bmi}</div>
          
          {isBmiHigh ? (
            <div className={styles.alertBox}>
              <strong>Uwaga!</strong> Twoje BMI wskazuje na nadwagę/otyłość. <a href="https://www.youtube.com/watch?v=DFhc3xqYKR8" target="_blank" >Poradnik do zrzucenia wagi</a> 
            </div>
          ) : (
            <div className={styles.successBox}>
              Twoja waga jest w normie. Tak trzymaj!
            </div>
          )}
        </div>
      </div>

      <div className={styles.actionsSection}>
        <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={() => console.log("History...")}>
          Zobacz historię badań
        </button>
        <button className={`${styles.btn} ${styles.btnOutline}`}>
          Wykonaj nowy test
        </button>
      </div>

        <section style={{ marginBottom: '2.5rem' }}>
            <h2 style={{ marginBottom: '1rem', color: '#456990' }}>Poradź się asystenta</h2>
            <HealthChat />
        </section>

    </div>
  );
};

export default UserProfile;