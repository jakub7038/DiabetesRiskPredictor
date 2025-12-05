import styles from '@/components/ui/RiskAssessmentCta/RiskAssessment.module.css'
import Button from '@/components/ui/Button/Button'


const RiskAssessmentCta = () => {
    return (
        <section className={styles.ctaSection}>
            <h2 className={styles.h2}>Poznaj swoje ryzyko</h2>
            <p>Skorzystaj z naszego bezpłatnego, szybkiego i internetowego narzędzia, aby sprawdzić ryzyko zachorowania na cukrzycę typu 2. Zajmie Ci to tylko kilka minut, a wyniki otrzymasz natychmiast.</p>
            <Button size="lg" variant="primary" className={styles.ctaButton}>
                <a href="/">Oblicz swoje ryzyko teraz</a>
            </Button>
        </section>
    )
}

export default RiskAssessmentCta