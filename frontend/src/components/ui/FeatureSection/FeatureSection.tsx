import styles from "./FeatureSection.module.css"


type FeatureSectionProps = {
    title: string,
    description: React.ReactNode,
    imageSrc: string,
    imageAlt: string
}

const FeatureSection = ({ title, description, imageSrc, imageAlt }: FeatureSectionProps) => {


    return (
        <>
            <section className={styles.section}>
                <h3 className={styles.title}>{title}</h3>
                
                {description}

                <div className={styles.imgContainer}>
                    <img
                        src={imageSrc}
                        alt={imageAlt}
                        className={styles.img}
                    />
                </div>

            </section>
        </>
    )
}

export default FeatureSection