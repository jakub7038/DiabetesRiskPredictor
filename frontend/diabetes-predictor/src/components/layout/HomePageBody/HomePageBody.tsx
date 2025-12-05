import styles from './HomePageBody.module.css'
import RiskAssessmentCta from '@/components/ui/RiskAssessmentCta/RiskAssessmentCta'

import diabeticImage from '@/assets/images/1400x854cukrzycauseniorow.png'

const HomePageBody = () => {
    return (
        <> 
            <main className={styles.main}>
                <div className={styles.container}>
                    <img className={styles.heroImage} src={diabeticImage} alt="obrazek przedstawiający osobę zmagającą sie z cukrzycą" />
                    <div className={styles.ctaOverlay}>
                        <RiskAssessmentCta />
                    </div>
                </div>             
            </main>
        </>
    )
}

export default HomePageBody