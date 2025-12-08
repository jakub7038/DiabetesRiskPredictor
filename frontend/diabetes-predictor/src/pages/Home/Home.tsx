import styles from './Home.module.css'
import Cta from '@/components/ui/Cta/Cta'

import diabeticImage from '@/assets/images/1400x854cukrzycauseniorow.png'

const Home = () => {
    return (
        <> 
            <main className={styles.main}>
                <div className={styles.container}>
                    <img className={styles.heroImage} src={diabeticImage} alt="obrazek przedstawiający osobę zmagającą sie z cukrzycą" />
                    <div className={styles.ctaOverlay}>
                        <Cta 
                            title="Poznaj swoje ryzyko"
                            description="Skorzystaj z naszego bezpłatnego, szybkiego i internetowego narzędzia, aby sprawdzić ryzyko zachorowania na cukrzycę typu 2. Zajmie Ci to tylko kilka minut, a wyniki otrzymasz natychmiast."
                            buttonText="Oblicz swoje ryzyko teraz"
                            buttonLink="/predyktor-ryzyka"
                        />
                    </div>
                </div>             
            </main>
        </>
    )
}

export default Home