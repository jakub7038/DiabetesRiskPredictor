import styles from './Cta.module.css'
import Button from '@/components/ui/Button/Button'

import { Link } from 'react-router-dom' 

type CtaProps = {
    title: string,
    description: string,
    buttonText: string,
    buttonLink: string
}

const Cta = ({title, description, buttonText, buttonLink }: CtaProps) => {
    return (
        <section className={styles.ctaSection}>
            <h2 className={styles.h2}>{title}</h2>
            <p>{description}</p>
            <Link to={buttonLink}>
                <Button size="lg" variant="primary" className={styles.ctaButton}>
                    {buttonText}
                </Button>
            </Link>
        </section>
    )
}

export default Cta