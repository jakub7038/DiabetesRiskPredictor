import styles from './Home.module.css'
import Cta from '@/components/ui/Cta/Cta'

import diabeticImage from '@/assets/images/1400x854cukrzycauseniorow.png'
import riskFactorImage from '@/assets/images/type_2_diabetes.png'
import actionImage from '@/assets/images/Browsing-searching-Actions800w.png.webp'

import FeatureSection from '@/components/ui/FeatureSection/FeatureSection'

const Home = () => {
    return (
        <>

            <div className={styles.container}>
                <img className={styles.heroImage} src={diabeticImage} alt="obrazek przedstawiający osobę zmagającą sie z cukrzycą" />
                <div className={styles.heroOverlay}></div>
                <div className={styles.ctaWrapper}>
                    <Cta
                        title="Poznaj swoje ryzyko"
                        description="Cukrzyca potrafi rozwijać się latami, nie dając żadnych objawów. Nie czekaj, aż organizm wyśle sygnał alarmowy. Zrób darmowy test przesiewowy online i dowiedz się, na czym stoisz."
                        buttonText="Oblicz swoje ryzyko teraz"
                        buttonLink="/predyktor-ryzyka"
                    />
                </div>
            </div>

            <FeatureSection title='Dlaczego warto się badać?'>
                <p>Cukrzyca nie boli, ale można ją wyprzedzić. Wiele osób żyje ze stanem przedcukrzycowym, nie wiedząc o tym.</p>
                <ul>
                    <li>
                        <span>🧠</span>
                        <strong>Wiedza to spokój:</strong> Poznaj prawdę o swoim zdrowiu zamiast się domyślać.
                    </li>
                    <li>
                        <span>⏳</span>
                        <strong>Czas na reakcję:</strong> Wykryta wcześnie cukrzyca typu 2 jest w dużej mierze odwracalna!
                    </li>
                    <li>
                        <span>🛡️</span>
                        <strong>Ochrona przyszłości:</strong> Uniknij groźnych powikłań (wzrok, nerki, serce), póki masz na to wpływ.
                    </li>
                </ul>
                <p className={styles.note}><em>To nie jest diagnoza lekarska, ale drogowskaz, który pokaże Ci, czy warto zrobić badania krwi.</em></p>
            </FeatureSection>

            <FeatureSection
                title='Kto powinien się zbadać?'
                isReversed={true}
                imageSrc={riskFactorImage}
                imageAlt='Obrazek otyłego osobnika z cukrzycą'
            >
                <p>Ryzyko to nie tylko słodycze. Sprawdź, czy dotyczy Cię choć jeden punkt:</p>
                <ul>
                    <li>🔴 Masz ponad 45 lat?</li>
                    <li>🔴 W Twojej rodzinie występowała cukrzyca?</li>
                    <li>🔴 Masz nadwagę lub otyłość brzuszną?</li>
                    <li>🔴 Prowadzisz siedzący tryb życia?</li>
                    <li>🔴 Masz nadciśnienie tętnicze?</li>
                </ul>
                <p>Jeśli na którekolwiek pytanie odpowiedziałeś <strong>TAK</strong> – ten test jest dla Ciebie.</p>
            </FeatureSection>

            <FeatureSection title='Jak to działa?'
                imageSrc={actionImage}
                imageAlt='Obrazek przedstawiający wypełnianie ankiety'
            >
                <p>Wystarczą 3 proste kroki do lepszego zdrowia:</p>

                <div className={styles.stepsContainer}>
                    <div className={styles.stepCard}>
                        <div className={styles.stepHeader}>
                            <span>📝</span>
                            <strong>1. Wypełnij ankietę</strong>
                        </div>
                        <p className={styles.stepDescription}>Odpowiedz na proste pytania. Bez podawania nazwiska.</p>
                    </div>
                    <div className={styles.stepCard}>
                        <div className={styles.stepHeader}>
                            <span>📊</span>
                            <strong>2. Odbierz wynik</strong>
                        </div>
                        <p className={styles.stepDescription}>Algorytm natychmiast obliczy Twoje ryzyko zachorowania.</p>
                    </div>
                    <div className={styles.stepCard}>
                        <div className={styles.stepHeader}>
                            <span>💡</span>
                            <strong>3. Dostań zalecenia</strong>
                        </div>
                        <p className={styles.stepDescription}>Dowiedz się, czy wystarczy zmiana diety, czy konieczna jest wizyta u lekarza.</p>
                    </div>
                </div>
            </FeatureSection>

        </>
    )
}

export default Home