import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './UserProfile.module.css';
import HealthChat from '@/components/HealthChat/HealthChat';
import { authService } from '@/api/authService';
import { useAuth } from '@/context/AuthContext';

interface UserData {
  sex: boolean;
  age: number;
  high_bp: boolean;
  high_chol: boolean;
  chol_check: boolean;
  smoker: boolean;
  stroke: boolean;
  heart_disease: boolean;
  any_healthcare: boolean;
  no_docbc_cost: boolean;
  diff_walk: boolean;
}

interface LastTestData {
  date: string;
  riskScore: number;
  riskLevel: 'Niskie' | 'Średnie' | 'Wysokie';
  bmi: number;
  weight: number;
  height: number;
}

const UserProfile: React.FC = () => {
  const navigate = useNavigate();
  const { isLoggedIn } = useAuth();
  const [userData, setUserData] = useState<UserData | null>(null);
  const [lastTest, setLastTest] = useState<LastTestData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<Partial<UserData>>({});

  useEffect(() => {
    if (!isLoggedIn) {
      navigate('/logowanie');
      return;
    }
    fetchUserData();
    fetchLastTest();
  }, [isLoggedIn]);

  const fetchUserData = async () => {
    try {
      const response = await authService.getUserData();
      if (response.data) {
        setUserData(response.data);
      }
    } catch (error: any) {
      console.error('Błąd pobierania danych:', error);
    }
  };

  const fetchLastTest = async () => {
    try {
      setIsLoading(true);
      const response = await authService.getHistory(1); // Pobierz tylko ostatni test
      
      if (response.data && response.data.length > 0) {
        const lastRecord = response.data[0];
        
        // Wyciągnij BMI, wagę i wzrost z input_data
        const inputData = lastRecord.input_data || {};
        const bmi = inputData.BMI || 0;
        const weight = inputData.Weight || 0;
        const height = inputData.Height || 0;
        
        // Określ poziom ryzyka na podstawie probability
        let riskLevel: 'Niskie' | 'Średnie' | 'Wysokie' = 'Niskie';
        if (lastRecord.probability >= 35) {
          riskLevel = 'Wysokie';
        } else if (lastRecord.probability >= 15) {
          riskLevel = 'Średnie';
        }
        
        setLastTest({
          date: lastRecord.created_at,
          riskScore: lastRecord.probability,
          riskLevel: riskLevel,
          bmi: bmi,
          weight: weight,
          height: height
        });
      }
    } catch (error: any) {
      console.error('Błąd pobierania ostatniego testu:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditData(userData || {});
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditData({});
  };

  const handleSave = async () => {
    try {
      await authService.saveUserData(editData);
      setUserData(editData as UserData);
      setIsEditing(false);
      alert('Dane zapisane pomyślnie!');
    } catch (error: any) {
      alert('Błąd zapisu danych: ' + error.message);
    }
  };

  const getDaysSinceTest = (dateString: string): number => {
    const testDate = new Date(dateString);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - testDate.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
  };

  const getAgeLabel = (ageCategory: number): string => {
    const ageRanges: Record<number, string> = {
      1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39",
      5: "40-44", 6: "45-49", 7: "50-54", 8: "55-59",
      9: "60-64", 10: "65-69", 11: "70-74", 12: "75-79",
      13: "80+"
    };
    return ageRanges[ageCategory] || "Nieznany";
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pl-PL', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };

  if (isLoading) {
    return (
      <div className={styles.profileContainer}>
        <p>Ładowanie danych...</p>
      </div>
    );
  }

  // Oblicz BMI z ostatniego testu lub z inputu
  const bmi = lastTest ? lastTest.bmi : 0;
  const isBmiHigh = bmi >= 25;
  const daysSince = lastTest ? getDaysSinceTest(lastTest.date) : null;

  return (
    <div className={styles.profileContainer}>
      <header className={styles.profileHeader}>
        <h1>Twój profil zdrowotny</h1>
        <p>Centrum monitorowania zdrowia</p>
      </header>

      <div className={styles.dashboardGrid}>
        {/* Karta Dane Użytkownika */}
        <div className={styles.card}>
          <div className={styles.cardHeaderRow}>
            <h3>Twoje Dane</h3>
            {!isEditing && (
              <button className={styles.editLink} onClick={handleEdit}>
                Edytuj
              </button>
            )}
          </div>
          
          {!userData && !isEditing ? (
            <div>
              <p>Brak zapisanych danych.</p>
              <button className={styles.btn} onClick={handleEdit}>
                Dodaj dane
              </button>
            </div>
          ) : isEditing ? (
            <div className={styles.editForm}>
              <div className={styles.formGroup}>
                <label>Płeć:</label>
                <select
                  value={editData.sex !== undefined ? (editData.sex ? "1" : "0") : ""}
                  onChange={(e) => setEditData({...editData, sex: e.target.value === "1"})}
                >
                  <option value="">Wybierz</option>
                  <option value="0">Kobieta</option>
                  <option value="1">Mężczyzna</option>
                </select>
              </div>

              <div className={styles.formGroup}>
                <label>Przedział wiekowy:</label>
                <select
                  value={editData.age || ""}
                  onChange={(e) => setEditData({...editData, age: parseInt(e.target.value)})}
                >
                  <option value="">Wybierz</option>
                  <option value="1">18-24</option>
                  <option value="2">25-29</option>
                  <option value="3">30-34</option>
                  <option value="4">35-39</option>
                  <option value="5">40-44</option>
                  <option value="6">45-49</option>
                  <option value="7">50-54</option>
                  <option value="8">55-59</option>
                  <option value="9">60-64</option>
                  <option value="10">65-69</option>
                  <option value="11">70-74</option>
                  <option value="12">75-79</option>
                  <option value="13">80+</option>
                </select>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.high_bp || false}
                    onChange={(e) => setEditData({...editData, high_bp: e.target.checked})}
                  />
                  Wysokie ciśnienie
                </label>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.high_chol || false}
                    onChange={(e) => setEditData({...editData, high_chol: e.target.checked})}
                  />
                  Wysoki cholesterol
                </label>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.smoker || false}
                    onChange={(e) => setEditData({...editData, smoker: e.target.checked})}
                  />
                  Palę papierosy
                </label>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.stroke || false}
                    onChange={(e) => setEditData({...editData, stroke: e.target.checked})}
                  />
                  Miałem/am udar
                </label>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.heart_disease || false}
                    onChange={(e) => setEditData({...editData, heart_disease: e.target.checked})}
                  />
                  Choroba serca
                </label>
              </div>

              <div className={styles.checkboxGroup}>
                <label>
                  <input
                    type="checkbox"
                    checked={editData.diff_walk || false}
                    onChange={(e) => setEditData({...editData, diff_walk: e.target.checked})}
                  />
                  Trudności z chodzeniem
                </label>
              </div>

              <div className={styles.formActions}>
                <button className={`${styles.btn} ${styles.btnPrimary}`} onClick={handleSave}>
                  Zapisz
                </button>
                <button className={`${styles.btn} ${styles.btnOutline}`} onClick={handleCancel}>
                  Anuluj
                </button>
              </div>
            </div>
          ) : (
            <ul className={styles.detailsList}>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Płeć:</span>
                <span className={styles.detailValue}>{userData!.sex ? 'Mężczyzna' : 'Kobieta'}</span>
              </li>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Wiek:</span>
                <span className={styles.detailValue}>{getAgeLabel(userData!.age)} lat</span>
              </li>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Wysokie ciśnienie:</span>
                <span className={styles.detailValue}>{userData!.high_bp ? 'Tak' : 'Nie'}</span>
              </li>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Wysoki cholesterol:</span>
                <span className={styles.detailValue}>{userData!.high_chol ? 'Tak' : 'Nie'}</span>
              </li>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Palenie:</span>
                <span className={styles.detailValue}>{userData!.smoker ? 'Tak' : 'Nie'}</span>
              </li>
              <li className={styles.detailRow}>
                <span className={styles.detailLabel}>Choroba serca:</span>
                <span className={styles.detailValue}>{userData!.heart_disease ? 'Tak' : 'Nie'}</span>
              </li>
            </ul>
          )}
        </div>

        {/* Karta Ryzyko Cukrzycy */}
        {lastTest ? (
          <div className={styles.card}>
            <h3>Twoje ryzyko cukrzycy</h3>
            <div className={styles.riskIndicator}>
              <span className={`${styles.riskValue} ${lastTest.riskLevel === 'Wysokie' ? styles.textWarning : ''}`}>
                {lastTest.riskLevel}
              </span>
              <div className={styles.progressBarBg}>
                <div 
                  className={styles.progressBarFill} 
                  style={{ width: `${lastTest.riskScore}%` }}
                ></div>
              </div>
              <p className={styles.scoreDetails}>{lastTest.riskScore}% w skali ryzyka</p>
            </div>
          </div>
        ) : (
          <div className={styles.card}>
            <h3>Twoje ryzyko cukrzycy</h3>
            <p className={styles.noDataText}>Brak danych. Wykonaj pierwszy test!</p>
            <button 
              className={`${styles.btn} ${styles.btnPrimary}`}
              onClick={() => navigate('/predyktor-ryzyka')}
            >
              Wykonaj test
            </button>
          </div>
        )}

        {/* Karta Ostatnie Badanie */}
        {lastTest && daysSince !== null ? (
          <div className={styles.card}>
            <h3>Ostatnie badanie</h3>
            <div className={styles.daysDisplay}>
              <span className={styles.daysNumber}>{daysSince}</span>
              <span className={styles.daysLabel}>dni temu</span>
            </div>
            <p className={styles.dateSubtext}>Data: {formatDate(lastTest.date)}</p>
          </div>
        ) : (
          <div className={styles.card}>
            <h3>Ostatnie badanie</h3>
            <p className={styles.noDataText}>Nie wykonałeś jeszcze żadnego testu.</p>
          </div>
        )}

        {/* Karta BMI */}
        {lastTest && bmi > 0 ? (
          <div className={`${styles.card} ${styles.bmiCard} ${isBmiHigh ? styles.warningBorder : ''}`}>
            <h3>Twoje BMI</h3>
            <div className={styles.bmiValue}>{bmi.toFixed(1)}</div>
            
            {isBmiHigh ? (
              <div className={styles.alertBox}>
                <strong>Uwaga!</strong> Twoje BMI wskazuje na nadwagę/otyłość. 
                <a href="https://www.youtube.com/watch?v=DFhc3xqYKR8" target="_blank">Poradnik do zrzucenia wagi</a> 
              </div>
            ) : (
              <div className={styles.successBox}>
                Twoja waga jest w normie. Tak trzymaj!
              </div>
            )}
            <p className={styles.bmiDetails}>
              Waga: {lastTest.weight} kg | Wzrost: {lastTest.height} cm
            </p>
          </div>
        ) : (
          <div className={styles.card}>
            <h3>Twoje BMI</h3>
            <p className={styles.noDataText}>Brak danych o BMI. Wykonaj test!</p>
          </div>
        )}
      </div>

      <div className={styles.actionsSection}>
        <button 
          className={`${styles.btn} ${styles.btnPrimary}`} 
          onClick={() => navigate('/historia')}
        >
          Zobacz historię badań
        </button>
        <button 
          className={`${styles.btn} ${styles.btnOutline}`}
          onClick={() => navigate('/predyktor-ryzyka')}
        >
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