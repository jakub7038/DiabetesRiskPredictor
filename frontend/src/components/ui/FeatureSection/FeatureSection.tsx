import styles from "./FeatureSection.module.css"
import React from 'react';

type FeatureSectionProps = {
    title: string,
    children: React.ReactNode, 
    imageSrc?: string,        
    imageAlt?: string,
    isReversed?: boolean      
}

const FeatureSection = ({ title, children, imageSrc, imageAlt, isReversed = false }: FeatureSectionProps) => {
    return (
        <section className={`${styles.section} ${isReversed ? styles.reversed : ''}`}>
            <div className={styles.content}>
                <h3 className={styles.title}>{title}</h3>
                <div className={styles.description}>
                    {children}
                </div>
            </div>

            {imageSrc && (
                <div className={styles.imgContainer}>
                    <img
                        src={imageSrc}
                        alt={imageAlt || title}
                        className={styles.img}
                    />
                </div>
            )}
        </section>
    )
}

export default FeatureSection